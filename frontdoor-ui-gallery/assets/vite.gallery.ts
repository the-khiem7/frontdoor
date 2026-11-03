// Template: a Vite config that serves the real frontend with the modules at
// the backend seam resolved to the gallery mocks. Save it beside the app's
// vite config as vite.gallery.config.ts, fill in MOCKS, point mockDir at the
// gallery mock folder (relative to this file), and add a script:
// "gallery": "vite --config vite.gallery.config.ts". Keep this file out of the
// frontend's type check: importing a .ts file by its extension fails tsc
// unless allowImportingTsExtensions is on, and Vite needs the extension.
import { fileURLToPath } from "node:url";
import { defineConfig, mergeConfig, type Plugin, type UserConfig, type ConfigEnv } from "vite";
import base from "./vite.config.ts";

const mockDir = fileURLToPath(new URL("./gallery/mock/", import.meta.url));

// Each entry: a pattern matched against the import specifier as written, and
// the mock file (in mockDir) that replaces it. Match the narrowest seam: the
// app's own wrapper module when it has one, else the generated bindings, else
// the platform package.
const MOCKS: [RegExp, (m: RegExpExecArray) => string][] = [
  // [/\/internal\/ui\/(service|settingsservice)(\.js)?$/, (m) => `${m[1]}.ts`],
  // [/\/lib\/ipc(\.ts)?$/, () => "ipc.ts"],
  // [/^@tauri-apps\/api\/event$/, () => "event.ts"],
];

function galleryMocks(): Plugin {
  const own = mockDir.replaceAll("\\", "/");
  return {
    name: "ui-gallery-mocks",
    enforce: "pre",
    resolveId(source, importer) {
      // A mock may import the real module's types; never redirect its own imports.
      if (importer?.replaceAll("\\", "/").startsWith(own)) return null;
      for (const [pattern, file] of MOCKS) {
        const m = pattern.exec(source);
        if (m) return mockDir + file(m);
      }
      return null;
    },
  };
}

// The port must match "base" in design/ui-gallery/gallery.json.
const gallery: UserConfig = {
  server: { port: Number(process.env.GALLERY_PORT) || 9246, strictPort: true },
  plugins: [galleryMocks()],
};

export default defineConfig((env: ConfigEnv) =>
  mergeConfig(typeof base === "function" ? (base as (e: ConfigEnv) => UserConfig)(env) : base, gallery),
);
