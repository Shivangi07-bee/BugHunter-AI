const { app, BrowserWindow } = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1500,
    height: 950,
    minWidth: 1200,
    minHeight: 750,

    title: "BugHunter AI",

    backgroundColor: "#070b14",

    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });

  // Load the BugHunter AI frontend.

if (process.env.NODE_ENV === "development") {
  mainWindow.loadURL("http://localhost:5173/");
} else {
  mainWindow.loadFile(
    path.join(process.resourcesPath, "frontend-dist", "index.html")
  );
}

  // Open DevTools only when explicitly needed.
  // mainWindow.webContents.openDevTools();

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});