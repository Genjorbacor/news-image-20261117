// News-image entry (Node 22, standard library only). The image is the
// entry.png beside this file: a front page drawn for 17 November 2026.
// The program copies it to the output directory the grader names, or
// /output when nothing is set. Copying bytes keeps the image identical
// on every run: the program never draws, fetches or changes anything.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
