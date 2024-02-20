import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import init from "./db/config.js";
import uR from "./routers/userRouter.js";
dotenv.config();

// express config
const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// test api
app.get("/test", (req, res) => {
  res.send("Hello World! Go To /api");
});

// base router
const bR = express.Router();
app.use("/api", bR);

bR.get("/", (req, res) => {
    res.send("v0.0.1");
});

// Routes /api/{route}
bR.use("/user", uR);

// start server
const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
    console.clear()
    init()
    console.log(`Server @ http://localhost:${PORT}`);
});