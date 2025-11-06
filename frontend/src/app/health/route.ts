import { NextResponse } from "next/server";

const VERSION = "0.1.0";

export const runtime = "edge";

export async function GET() {
  return NextResponse.json({ status: "ok", version: VERSION });
}
