import { NextRequest, NextResponse } from "next/server";

const SELF = "'self'";
const IMG_SRC = ["'self'", "data:"];
const FONT_SRC = ["'self'", "data:"];

function shouldForceProd(request: NextRequest) {
  return (
    process.env.FORCE_CSP_PROD === "true" ||
    request.headers.get("x-csp-force-prod") === "true"
  );
}

export function middleware(request: NextRequest) {
  const nonce = crypto.randomUUID().replace(/-/g, "");
  const forcedProd = shouldForceProd(request);
  const isDev = !forcedProd && process.env.NODE_ENV !== "production";
  const styleSrc = isDev ? `${SELF} 'unsafe-inline'` : `${SELF} 'nonce-${nonce}'`;

  if (!isDev && styleSrc.includes("unsafe-inline")) {
    console.error(
      "[CSP] unsafe-inline detected in production environment. Blocking response."
    );
    return new NextResponse("CSP violation detected", { status: 500 });
  }

  const directives = [
    `default-src ${SELF}`,
    `script-src ${SELF}`,
    `style-src ${styleSrc}`,
    `img-src ${IMG_SRC.join(" ")}`,
    `font-src ${FONT_SRC.join(" ")}`,
    "object-src 'none'",
    "base-uri 'self'",
    "frame-ancestors 'none'",
    `connect-src ${SELF}`,
  ].join("; ");

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-csp-nonce", nonce);

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });

  response.headers.set("Content-Security-Policy", directives);
  response.headers.set("X-CSP-Nonce", nonce);
  if (forcedProd) {
    response.headers.set("X-CSP-Mode", "forced-production");
  }

  return response;
}

export const config = {
  matcher: "/:path*",
};
