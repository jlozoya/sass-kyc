import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import eslintConfigPrettier from "eslint-config-prettier";
import globals from "globals";

export default tseslint.config(
  // Ignorar build / deps
  {
    ignores: ["dist/**", "node_modules/**", "coverage/**"],
  },

  // Reglas base JS
  eslint.configs.recommended,

  // Reglas TS
  ...tseslint.configs.recommended,

  // Reglas Vue 3 (flat) -> incluye vue-eslint-parser
  ...pluginVue.configs["flat/recommended"],

  // 👇 Aseguramos que los .vue usen TS para el <script> interno
  {
    files: ["**/*.vue"],
    languageOptions: {
      parserOptions: {
        // vue-eslint-parser ya viene desde pluginVue,
        // aquí solo le decimos que use TS para el <script>
        parser: tseslint.parser,
        ecmaVersion: "latest",
        sourceType: "module",
        extraFileExtensions: [".vue"],
      },
    },
  },

  // Config general para JS/TS/Vue: globals + reglas
  {
    files: ["**/*.{js,ts,vue}"],
    plugins: {
      "@typescript-eslint": tseslint.plugin,
    },
    languageOptions: {
      globals: {
        ...globals.browser, // navigator, window, etc.
        ...globals.es2021,
      },
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
    },
  },

  // Prettier al final
  eslintConfigPrettier
);
