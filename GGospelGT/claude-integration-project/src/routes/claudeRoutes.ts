import { Router } from 'express';
import ClaudeController from '../controllers/claudeController';

const router = Router();
const claudeController = new ClaudeController();

export function setClaudeRoutes(app) {
    app.use('/claude', router);

    router.post('/process', claudeController.processRequest.bind(claudeController));
    router.get('/response', claudeController.getResponse.bind(claudeController));
}