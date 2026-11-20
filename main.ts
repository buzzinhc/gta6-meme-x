// Entry program for the make.fun bounty "gta6-meme-x-01".
//
// The entry itself is a public post on X; this program hands in the proof.
// It copies POST.json — a small file at the repository root naming the post's
// URL — into the output directory, where the grader reads it. The meme image
// (meme.png) and the post text (post.txt) stay in the repository as the
// record of what was posted.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(process.cwd(), "POST.json");

function main(): void {
  if (!existsSync(source)) {
    throw new Error(`POST.json not found at ${source}`);
  }

  // Parse before copying: a malformed pointer should fail here, loudly,
  // rather than hand the grader a file it cannot read.
  const post = JSON.parse(readFileSync(source, "utf8")) as { url?: unknown };
  if (typeof post.url !== "string" || !post.url.startsWith("https://x.com/")) {
    throw new Error(`POST.json must name an https://x.com/ post URL`);
  }

  mkdirSync(outputDir, { recursive: true });
  const target = join(outputDir, "POST.json");
  copyFileSync(source, target);
  console.log(`handed in ${target} -> ${post.url}`);
}

main();
