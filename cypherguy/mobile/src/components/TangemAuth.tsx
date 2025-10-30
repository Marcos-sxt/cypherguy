/**
 * TangemAuth Component
 * Handles complete Tangem wallet authentication flow
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  Platform,
} from 'react-native';
import { tangemService, TangemCard } from '../services/TangemService';

interface TangemAuthProps {
  onAuthSuccess: (card: TangemCard) => void;
  onAuthFailure?: (error: string) => void;
}

export const TangemAuth: React.FC<TangemAuthProps> = ({
  onAuthSuccess,
  onAuthFailure,
}) => {
  const [loading, setLoading] = useState(false);
  const [card, setCard] = useState<TangemCard | null>(null);
  const [nfcAvailable, setNfcAvailable] = useState<boolean | null>(null);
  const [useMock, setUseMock] = useState(true);

  useEffect(() => {
    checkNFCAvailability();
  }, []);

  const checkNFCAvailability = async () => {
    try {
      const available = await tangemService.checkNFCAvailability();
      setNfcAvailable(available);
      console.log('NFC Available:', available);
    } catch (error) {
      console.error('NFC check failed:', error);
      setNfcAvailable(false);
    }
  };

  const handleAuthenticate = async () => {
    setLoading(true);
    try {
      console.log('🔐 Starting Tangem authentication...');

      // Step 1: Scan card
      Alert.alert(
        '💳 Tangem Card',
        useMock
          ? 'Simulando leitura do cartão NFC...'
          : 'Aproxime seu cartão Tangem do telefone',
        [{ text: 'OK' }]
      );

      const scannedCard = await tangemService.scanCard();
      console.log('✅ Card scanned:', scannedCard);
      setCard(scannedCard);

      // Step 2: Authenticate (challenge-response)
      console.log('🔐 Authenticating user...');
      const authResult = await tangemService.authenticateUser();
      console.log('✅ Authentication successful:', authResult);

      // Step 3: Success callback
      onAuthSuccess(scannedCard);

      Alert.alert(
        '✅ Autenticação Bem-Sucedida!',
        `Cartão: ${scannedCard.cardId}\n` +
        `Blockchain: ${scannedCard.blockchain.toUpperCase()}\n` +
        `Status: ${scannedCard.status}\n\n` +
        `Você está pronto para usar o CypherGuy!`,
        [{ text: 'Continuar' }]
      );

    } catch (error: any) {
      console.error('❌ Authentication failed:', error);
      
      const errorMessage = error.message || 'Authentication failed';
      
      if (onAuthFailure) {
        onAuthFailure(errorMessage);
      }

      Alert.alert(
        '❌ Erro de Autenticação',
        errorMessage,
        [
          {
            text: 'Tentar Novamente',
            onPress: () => handleAuthenticate(),
          },
          { text: 'Cancelar', style: 'cancel' },
        ]
      );
    } finally {
      setLoading(false);
    }
  };

  const handleToggleMockMode = () => {
    const newMode = !useMock;
    setUseMock(newMode);
    tangemService.setMockMode(newMode);
    
    Alert.alert(
      '🎭 Modo Alterado',
      newMode
        ? '✅ Modo Simulado ativado\nFunciona sem cartão físico'
        : '💳 Modo Real ativado\nRequer cartão Tangem e NFC',
      [{ text: 'OK' }]
    );
  };

  const handleDisconnect = () => {
    Alert.alert(
      '⚠️ Desconectar Cartão?',
      'Você perderá a autenticação atual.',
      [
        {
          text: 'Sim, Desconectar',
          style: 'destructive',
          onPress: () => {
            tangemService.clearCard();
            setCard(null);
            Alert.alert('✅ Desconectado', 'Cartão Tangem desconectado');
          },
        },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>💳 Tangem Wallet</Text>
        <Text style={styles.headerSubtitle}>
          Hardware Wallet Authentication
        </Text>
      </View>

      {/* Mode Toggle */}
      <TouchableOpacity
        style={styles.modeToggle}
        onPress={handleToggleMockMode}
      >
        <Text style={styles.modeLabel}>
          {useMock ? '🎭 Modo: Simulado' : '💳 Modo: Real'}
        </Text>
        <Text style={styles.modeDescription}>
          {useMock
            ? 'Tap para usar cartão físico'
            : 'Tap para simular (sem cartão)'}
        </Text>
      </TouchableOpacity>

      {/* NFC Status */}
      {!useMock && nfcAvailable !== null && (
        <View style={[
          styles.nfcStatus,
          nfcAvailable ? styles.nfcAvailable : styles.nfcUnavailable
        ]}>
          <Text style={styles.nfcStatusText}>
            {nfcAvailable
              ? '✅ NFC Disponível'
              : '⚠️ NFC Não Disponível'}
          </Text>
          {!nfcAvailable && (
            <Text style={styles.nfcStatusHint}>
              Habilite NFC nas configurações do dispositivo
            </Text>
          )}
        </View>
      )}

      {/* Card Status */}
      {card ? (
        <View style={styles.cardConnected}>
          <Text style={styles.connectedTitle}>✅ Cartão Conectado</Text>
          
          <View style={styles.cardDetails}>
            <View style={styles.cardDetailRow}>
              <Text style={styles.cardDetailLabel}>Card ID:</Text>
              <Text style={styles.cardDetailValue}>{card.cardId}</Text>
            </View>
            
            <View style={styles.cardDetailRow}>
              <Text style={styles.cardDetailLabel}>Public Key:</Text>
              <Text style={styles.cardDetailValue} numberOfLines={1}>
                {card.publicKey.substring(0, 20)}...
              </Text>
            </View>
            
            <View style={styles.cardDetailRow}>
              <Text style={styles.cardDetailLabel}>Blockchain:</Text>
              <Text style={styles.cardDetailValue}>
                {card.blockchain.toUpperCase()}
              </Text>
            </View>
            
            <View style={styles.cardDetailRow}>
              <Text style={styles.cardDetailLabel}>Status:</Text>
              <Text style={[
                styles.cardDetailValue,
                card.status === 'active' ? styles.statusActive : styles.statusLocked
              ]}>
                {card.status === 'active' ? 'Ativo' : 'Bloqueado (PIN)'}
              </Text>
            </View>

            {card.firmwareVersion && (
              <View style={styles.cardDetailRow}>
                <Text style={styles.cardDetailLabel}>Firmware:</Text>
                <Text style={styles.cardDetailValue}>
                  v{card.firmwareVersion}
                </Text>
              </View>
            )}

            {card.manufacturer && (
              <View style={styles.cardDetailRow}>
                <Text style={styles.cardDetailLabel}>Fabricante:</Text>
                <Text style={styles.cardDetailValue}>
                  {card.manufacturer}
                </Text>
              </View>
            )}
          </View>

          <TouchableOpacity
            style={[styles.button, styles.disconnectButton]}
            onPress={handleDisconnect}
          >
            <Text style={styles.buttonText}>🔌 Desconectar Cartão</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.cardDisconnected}>
          <Text style={styles.disconnectedTitle}>⚠️ Não Conectado</Text>
          <Text style={styles.disconnectedDescription}>
            {useMock
              ? 'Toque no botão abaixo para simular\numa leitura de cartão Tangem'
              : 'Aproxime seu cartão Tangem do\ntelefone para autenticar'}
          </Text>

          <TouchableOpacity
            style={[styles.button, styles.connectButton]}
            onPress={handleAuthenticate}
            disabled={loading || (!useMock && nfcAvailable === false)}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <>
                <Text style={styles.buttonText}>
                  {useMock ? '🎭 Simular Leitura' : '💳 Conectar Tangem'}
                </Text>
                <Text style={styles.buttonHint}>
                  {useMock
                    ? 'Autenticação simulada'
                    : 'Aproxime o cartão'}
                </Text>
              </>
            )}
          </TouchableOpacity>

          {!useMock && Platform.OS === 'android' && (
            <Text style={styles.platformHint}>
              📱 Android: Certifique-se que NFC está habilitado
            </Text>
          )}
          {!useMock && Platform.OS === 'ios' && (
            <Text style={styles.platformHint}>
              📱 iOS: iPhone 7+ com NFC requerido
            </Text>
          )}
        </View>
      )}

      {/* Info Box */}
      <View style={styles.infoBox}>
        <Text style={styles.infoTitle}>ℹ️ Sobre Tangem</Text>
        <Text style={styles.infoText}>
          • Hardware wallet em formato de cartão{'\n'}
          • EAL6+ certified secure element{'\n'}
          • Chave privada nunca sai do chip{'\n'}
          • Comunicação via NFC criptografado{'\n'}
          • Backup físico (múltiplos cartões)
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#8b92a8',
  },
  modeToggle: {
    backgroundColor: '#1a1f2e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#2a2f3e',
    alignItems: 'center',
  },
  modeLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  modeDescription: {
    fontSize: 12,
    color: '#8b92a8',
  },
  nfcStatus: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
    alignItems: 'center',
  },
  nfcAvailable: {
    backgroundColor: 'rgba(76, 175, 80, 0.1)',
    borderWidth: 1,
    borderColor: '#4caf50',
  },
  nfcUnavailable: {
    backgroundColor: 'rgba(255, 152, 0, 0.1)',
    borderWidth: 1,
    borderColor: '#ff9800',
  },
  nfcStatusText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  nfcStatusHint: {
    color: '#8b92a8',
    fontSize: 12,
    marginTop: 4,
  },
  cardConnected: {
    backgroundColor: '#1a1f2e',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#4caf50',
  },
  connectedTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4caf50',
    marginBottom: 16,
    textAlign: 'center',
  },
  cardDetails: {
    marginBottom: 16,
  },
  cardDetailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2f3e',
  },
  cardDetailLabel: {
    fontSize: 14,
    color: '#8b92a8',
    fontWeight: '600',
  },
  cardDetailValue: {
    fontSize: 14,
    color: '#fff',
    flex: 1,
    textAlign: 'right',
  },
  statusActive: {
    color: '#4caf50',
  },
  statusLocked: {
    color: '#ff9800',
  },
  cardDisconnected: {
    backgroundColor: '#1a1f2e',
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#ff9800',
    alignItems: 'center',
  },
  disconnectedTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ff9800',
    marginBottom: 8,
  },
  disconnectedDescription: {
    fontSize: 14,
    color: '#8b92a8',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 20,
  },
  button: {
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    minHeight: 56,
    justifyContent: 'center',
  },
  connectButton: {
    backgroundColor: '#2196f3',
    width: '100%',
  },
  disconnectButton: {
    backgroundColor: '#f44336',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  buttonHint: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 12,
    marginTop: 4,
  },
  platformHint: {
    fontSize: 12,
    color: '#8b92a8',
    marginTop: 12,
    textAlign: 'center',
  },
  infoBox: {
    backgroundColor: 'rgba(33, 150, 243, 0.1)',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(33, 150, 243, 0.3)',
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2196f3',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 12,
    color: '#8b92a8',
    lineHeight: 18,
  },
});

