import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const starterRoot = fileURLToPath(new URL('../../src/features/', import.meta.url));
export async function loadFeature(name) {
  const root = process.env.WORKSHOP_FEATURE_ROOT ?? starterRoot;
  return import(pathToFileURL(join(root, `${name}.mjs`)).href);
}

export async function loadAllFeatures() {
  const modules = await Promise.all(['priority', 'search', 'summary', 'handoff'].map(loadFeature));
  return Object.assign({}, ...modules);
}
