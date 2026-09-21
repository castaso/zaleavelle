// supabase/functions/shopee-sync/index.ts
// Pull-on-demand product data from a Shopee listing URL.
// POST { url } -> { name, price (IDR), image, stock, shopid, itemid, resolved }
// or { error, ... }. Manual panel fields always win — this only fills the form.
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36";

function cors() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
  };
}

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors(), "Content-Type": "application/json" },
  });
}

function extractIds(url: string): { shopid: string; itemid: string } | null {
  const m = url.match(/i\.(\d+)\.(\d+)/);
  return m ? { shopid: m[1], itemid: m[2] } : null;
}

serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors() });
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  try {
    const { url } = (await req.json()) as { url?: unknown };
    if (!url || typeof url !== "string") return json({ error: "url required" }, 400);

    let finalUrl = url;
    let ids = extractIds(url);
    if (!ids) {
      // Follow short-link redirects (e.g. s.shopee.co.id) to reach the item URL.
      const r = await fetch(url, {
        redirect: "follow",
        headers: { "User-Agent": UA },
      });
      finalUrl = r.url;
      await r.body?.cancel();
      ids = extractIds(finalUrl);
    }
    if (!ids) return json({ error: "no shopid/itemid in URL", resolved: finalUrl }, 422);

    const api =
      `https://shopee.co.id/api/v4/item/get?itemid=${ids.itemid}&shopid=${ids.shopid}`;
    const ir = await fetch(api, {
      headers: {
        "User-Agent": UA,
        Accept: "application/json",
        Referer: "https://shopee.co.id/",
      },
    });
    if (!ir.ok) {
      return json({ error: "shopee rejected request", status: ir.status, resolved: finalUrl }, 502);
    }
    const data = await ir.json();
    const item = data?.data;
    if (!item) return json({ error: "item not found", resolved: finalUrl }, 404);

    // Shopee v4 prices are integer IDR × 100000.
    const price = typeof item.price === "number" ? Math.round(item.price / 100000) : 0;
    const image = item.image
      ? `https://down-id.img.susercontent.com/file/${item.image}`
      : "";
    return json({
      name: item.name || "",
      price,
      image,
      stock: typeof item.stock === "number" ? item.stock : null,
      shopid: ids.shopid,
      itemid: ids.itemid,
      resolved: finalUrl,
    });
  } catch (e) {
    return json({ error: String((e as Error)?.message || e) }, 500);
  }
});
