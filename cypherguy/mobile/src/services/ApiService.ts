/**
 * API Service
 * Handles communication with CypherGuy backend
 */

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Change for production

export interface CreditRequest {
  user_id: string;
  amount: number;
  token: string;
  collateral: number;
}

export interface CreditResponse {
  user_id: string;
  amount: number;
  approved: boolean;
  interest_rate: number;
  tx_signature?: string;
  message: string;
}

export interface RWARequest {
  user_id: string;
  token_id: string;
  amount: number;
}

export interface RWAResponse {
  user_id: string;
  token_id: string;
  compliant: boolean;
  tx_signature?: string;
  message: string;
}

export interface TradeRequest {
  user_id: string;
  order_type: 'buy' | 'sell';
  amount: number;
  price: number;
}

export interface TradeResponse {
  user_id: string;
  order_type: string;
  matched: boolean;
  tx_signature?: string;
  message: string;
}

export interface AutomationRequest {
  user_id: string;
  portfolio_value: number;
  strategy: string;
}

export interface AutomationResponse {
  user_id: string;
  strategy: string;
  executed: boolean;
  tx_signature?: string;
  message: string;
}

export class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Add response interceptor
    this.client.interceptors.response.use(
      (response) => {
        console.log(`✅ API Response: ${response.status}`);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Request private DeFi credit
   */
  async requestCredit(request: CreditRequest): Promise<CreditResponse> {
    try {
      const response = await this.client.post<CreditResponse>('/credit', request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to request credit');
    }
  }

  /**
   * Request RWA compliance check
   */
  async requestRWA(request: RWARequest): Promise<RWAResponse> {
    try {
      const response = await this.client.post<RWAResponse>('/rwa', request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to request RWA');
    }
  }

  /**
   * Execute dark pool trade
   */
  async executeTrade(request: TradeRequest): Promise<TradeResponse> {
    try {
      const response = await this.client.post<TradeResponse>('/trade', request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to execute trade');
    }
  }

  /**
   * Set up DeFi automation
   */
  async setupAutomation(request: AutomationRequest): Promise<AutomationResponse> {
    try {
      const response = await this.client.post<AutomationResponse>('/automation', request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to setup automation');
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await this.client.get('/');
      return response.data;
    } catch (error: any) {
      throw new Error('Backend is not responding');
    }
  }
}

export const apiService = new ApiService();

