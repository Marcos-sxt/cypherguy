/**
 * CypherGuy Mobile App
 * React Native application with Tangem Wallet Authentication
 */

import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { TangemAuth } from './src/components/TangemAuth';
import { TangemCard } from './src/services/TangemService';
import { apiService } from './src/services/ApiService';

export default function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [card, setCard] = useState<TangemCard | null>(null);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [showAuth, setShowAuth] = useState(true);

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.healthCheck();
      setBackendStatus('online');
    } catch (error) {
      setBackendStatus('offline');
      Alert.alert(
        '⚠️ Backend Offline',
        'O backend não está respondendo.\nCertifique-se de que está rodando em http://localhost:8000'
      );
    }
  };

  const handleAuthSuccess = (authenticatedCard: TangemCard) => {
    setCard(authenticatedCard);
    setAuthenticated(true);
    setShowAuth(false);
  };

  const handleAuthFailure = (error: string) => {
    console.error('Authentication failed:', error);
  };

  const handleLogout = () => {
    Alert.alert(
      '🔓 Desconectar?',
      'Você precisará autenticar novamente com o cartão Tangem.',
      [
        {
          text: 'Sim, Desconectar',
          style: 'destructive',
          onPress: () => {
            setAuthenticated(false);
            setCard(null);
            setShowAuth(true);
          },
        },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  const handleCreditRequest = async () => {
    if (!card) {
      Alert.alert('⚠️ Erro', 'Cartão Tangem não conectado');
      return;
    }

    setLoading(true);
    try {
      const result = await apiService.requestCredit({
        user_id: card.cardId,
        amount: 1000,
        token: 'USDC',
        collateral: 1500,
      });

      Alert.alert(
        result.approved ? '✅ Crédito Aprovado' : '❌ Crédito Negado',
        `Usuário: ${card.cardId}\n` +
        `Valor: $${result.amount}\n` +
        `Taxa de Juros: ${result.interest_rate}%\n\n` +
        `${result.message}`,
        [{ text: 'OK' }]
      );
    } catch (error: any) {
      Alert.alert('❌ Erro', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRWARequest = async () => {
    if (!card) {
      Alert.alert('⚠️ Erro', 'Cartão Tangem não conectado');
      return;
    }

    setLoading(true);
    try {
      const result = await apiService.requestRWA({
        user_id: card.cardId,
        token_id: 'RWA-001',
        amount: 5000,
      });

      Alert.alert(
        result.compliant ? '✅ Compliance OK' : '❌ Compliance Falhou',
        `Token: ${result.token_id}\n\n${result.message}`,
        [{ text: 'OK' }]
      );
    } catch (error: any) {
      Alert.alert('❌ Erro', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTrade = async () => {
    if (!card) {
      Alert.alert('⚠️ Erro', 'Cartão Tangem não conectado');
      return;
    }

    setLoading(true);
    try {
      const result = await apiService.executeTrade({
        user_id: card.cardId,
        order_type: 'buy',
        amount: 0.5,
        price: 50000,
      });

      Alert.alert(
        result.matched ? '✅ Trade Executado' : '⏳ Ordem Pendente',
        result.message,
        [{ text: 'OK' }]
      );
    } catch (error: any) {
      Alert.alert('❌ Erro', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAutomation = async () => {
    if (!card) {
      Alert.alert('⚠️ Erro', 'Cartão Tangem não conectado');
      return;
    }

    setLoading(true);
    try {
      const result = await apiService.setupAutomation({
        user_id: card.cardId,
        portfolio_value: 10000,
        strategy: 'yield_farming',
      });

      Alert.alert(
        result.executed ? '✅ Automação Ativa' : '⏳ Configurando',
        `Estratégia: ${result.strategy}\n\n${result.message}`,
        [{ text: 'OK' }]
      );
    } catch (error: any) {
      Alert.alert('❌ Erro', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>🔐 CypherGuy</Text>
          <Text style={styles.subtitle}>
            Private AI-Powered DeFi Agent
          </Text>
          <View style={styles.statusContainer}>
            <View style={[
              styles.statusDot,
              backendStatus === 'online' ? styles.statusOnline : 
              backendStatus === 'offline' ? styles.statusOffline : 
              styles.statusChecking
            ]} />
            <Text style={styles.statusText}>
              Backend: {backendStatus === 'checking' ? 'Verificando...' : backendStatus}
            </Text>
          </View>
        </View>

        {/* Authentication Section */}
        {showAuth || !authenticated ? (
          <TangemAuth
            onAuthSuccess={handleAuthSuccess}
            onAuthFailure={handleAuthFailure}
          />
        ) : (
          <>
            {/* User Info Card */}
            <View style={styles.userCard}>
              <View style={styles.userHeader}>
                <Text style={styles.userTitle}>👤 Usuário Autenticado</Text>
                <TouchableOpacity
                  style={styles.logoutButton}
                  onPress={handleLogout}
                >
                  <Text style={styles.logoutText}>🔓 Sair</Text>
                </TouchableOpacity>
              </View>
              
              <View style={styles.userDetails}>
                <Text style={styles.userLabel}>Card ID:</Text>
                <Text style={styles.userValue}>{card?.cardId}</Text>
              </View>
              
              <View style={styles.userDetails}>
                <Text style={styles.userLabel}>Blockchain:</Text>
                <Text style={styles.userValue}>
                  {card?.blockchain.toUpperCase()}
                </Text>
              </View>

              <TouchableOpacity
                style={styles.showAuthButton}
                onPress={() => setShowAuth(!showAuth)}
              >
                <Text style={styles.showAuthText}>
                  {showAuth ? '▼ Ocultar Detalhes' : '▶ Mostrar Detalhes do Cartão'}
                </Text>
              </TouchableOpacity>
            </View>

            {showAuth && (
              <TangemAuth
                onAuthSuccess={handleAuthSuccess}
                onAuthFailure={handleAuthFailure}
              />
            )}

            {/* Features Section */}
            <View style={styles.featuresContainer}>
              <Text style={styles.sectionTitle}>🚀 Features</Text>
              <Text style={styles.sectionSubtitle}>
                Autenticado com Tangem • Todas features desbloqueadas
              </Text>

              <TouchableOpacity
                style={[styles.button, styles.featureButton]}
                onPress={handleCreditRequest}
                disabled={loading || backendStatus !== 'online'}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <>
                    <Text style={styles.featureEmoji}>💰</Text>
                    <Text style={styles.featureText}>Private DeFi Credit</Text>
                    <Text style={styles.featureDesc}>
                      Request credit with private KYC
                    </Text>
                  </>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.button, styles.featureButton]}
                onPress={handleRWARequest}
                disabled={loading || backendStatus !== 'online'}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <>
                    <Text style={styles.featureEmoji}>🏢</Text>
                    <Text style={styles.featureText}>RWA Compliance</Text>
                    <Text style={styles.featureDesc}>
                      Verify RWA token compliance
                    </Text>
                  </>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.button, styles.featureButton]}
                onPress={handleTrade}
                disabled={loading || backendStatus !== 'online'}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <>
                    <Text style={styles.featureEmoji}>🔄</Text>
                    <Text style={styles.featureText}>Dark Pool Trading</Text>
                    <Text style={styles.featureDesc}>Execute private trades</Text>
                  </>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.button, styles.featureButton]}
                onPress={handleAutomation}
                disabled={loading || backendStatus !== 'online'}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" size="small" />
                ) : (
                  <>
                    <Text style={styles.featureEmoji}>🤖</Text>
                    <Text style={styles.featureText}>DeFi Automation</Text>
                    <Text style={styles.featureDesc}>
                      Set up automated strategies
                    </Text>
                  </>
                )}
              </TouchableOpacity>
            </View>
          </>
        )}

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            🏆 Built for Solana Hackathon 2025
          </Text>
          <Text style={styles.footerText}>
            ASI Alliance • Arcium • Tangem • Solana
          </Text>
          <Text style={styles.footerVersion}>
            v1.0.0 • Tangem SDK Integrated
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0e1a',
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#8b92a8',
    marginBottom: 16,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  statusOnline: {
    backgroundColor: '#4caf50',
  },
  statusOffline: {
    backgroundColor: '#f44336',
  },
  statusChecking: {
    backgroundColor: '#ff9800',
  },
  statusText: {
    color: '#8b92a8',
    fontSize: 12,
  },
  userCard: {
    backgroundColor: '#1a1f2e',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#4caf50',
  },
  userHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  userTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4caf50',
  },
  logoutButton: {
    backgroundColor: 'rgba(244, 67, 54, 0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#f44336',
  },
  logoutText: {
    color: '#f44336',
    fontSize: 12,
    fontWeight: '600',
  },
  userDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  userLabel: {
    color: '#8b92a8',
    fontSize: 14,
  },
  userValue: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  showAuthButton: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#2a2f3e',
    alignItems: 'center',
  },
  showAuthText: {
    color: '#2196f3',
    fontSize: 14,
    fontWeight: '600',
  },
  featuresContainer: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  sectionSubtitle: {
    fontSize: 12,
    color: '#4caf50',
    marginBottom: 16,
  },
  button: {
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 56,
  },
  featureButton: {
    backgroundColor: '#1a1f2e',
    borderWidth: 1,
    borderColor: '#2a2f3e',
    marginBottom: 12,
    alignItems: 'flex-start',
    paddingVertical: 20,
  },
  featureEmoji: {
    fontSize: 32,
    marginBottom: 8,
  },
  featureText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 4,
  },
  featureDesc: {
    color: '#8b92a8',
    fontSize: 14,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  footerText: {
    color: '#8b92a8',
    fontSize: 12,
    marginTop: 4,
  },
  footerVersion: {
    color: '#4caf50',
    fontSize: 10,
    marginTop: 8,
  },
});
