import express from 'express';
import dotenv from 'dotenv';
import auth from '../middlewares/auth.js';
import UserController from '../controllers/userController.js';
dotenv.config();

const uR = express.Router();

const uC = new UserController();

uR.post('/testing', auth, uC.testing);

export default uR;