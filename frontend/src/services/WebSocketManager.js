class WebSocketManager {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.isConnecting = false;
    
    // Event handlers
    this.onConnectHandler = null;
    this.onDisconnectHandler = null;
    this.onMessageHandler = null;
    this.onErrorHandler = null;
  }

  connect() {
    if (this.isConnecting || this.ws?.readyState === WebSocket.OPEN) {
      return;
    }

    this.isConnecting = true;
    
    try {
      this.ws = new WebSocket('ws://localhost:8000/ws');
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        
        if (this.onConnectHandler) {
          this.onConnectHandler();
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason);
        this.isConnecting = false;
        
        if (this.onDisconnectHandler) {
          this.onDisconnectHandler();
        }

        // Attempt to reconnect if not manually closed
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.scheduleReconnect();
        }
      };

      this.ws.onmessage = (event) => {
        if (this.onMessageHandler) {
          this.onMessageHandler(event.data);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
        
        if (this.onErrorHandler) {
          this.onErrorHandler(error);
        }
      };

    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.isConnecting = false;
      
      if (this.onErrorHandler) {
        this.onErrorHandler(error);
      }
    }
  }

  scheduleReconnect() {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`Scheduling WebSocket reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);
    
    setTimeout(() => {
      if (this.ws?.readyState !== WebSocket.OPEN) {
        this.connect();
      }
    }, delay);
  }

  disconnect() {
    if (this.ws) {
      this.ws.close(1000, 'Manual disconnect');
      this.ws = null;
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      console.warn('WebSocket is not connected');
    }
  }

  // Event handler setters
  onConnect(handler) {
    this.onConnectHandler = handler;
  }

  onDisconnect(handler) {
    this.onDisconnectHandler = handler;
  }

  onMessage(handler) {
    this.onMessageHandler = handler;
  }

  onError(handler) {
    this.onErrorHandler = handler;
  }

  // Get connection status
  getStatus() {
    if (!this.ws) {
      return 'disconnected';
    }
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting';
      case WebSocket.OPEN:
        return 'connected';
      case WebSocket.CLOSING:
        return 'closing';
      case WebSocket.CLOSED:
        return 'closed';
      default:
        return 'unknown';
    }
  }

  // Check if connected
  isConnected() {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

export default WebSocketManager;