import express from "express";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
const port = process.env.PORT || 8080;

app.get("/config.js", (_request, response) => {
  response.type("application/javascript");
  response.send(
    `window.__MYWAY_CONFIG__ = ${JSON.stringify({
      apiBaseUrl: process.env.API_BASE_URL || "http://127.0.0.1:8000",
    })};`,
  );
});

app.use(express.static(path.join(__dirname, "dist")));

app.get("/{*splat}", (_request, response) => {
  response.sendFile(path.join(__dirname, "dist", "index.html"));
});

app.listen(port, "0.0.0.0", () => {
  console.log(`MyWay AI frontend listening on ${port}`);
});
