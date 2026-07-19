const API_BASE = 'http://localhost:8000/api';

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

export async function getDashboardSnapshot() {
  return fetchAPI('/dashboard/snapshot');
}

export async function getExecutiveSummary() {
  return fetchAPI('/executive-summary');
}

export async function getInventory() {
  return fetchAPI('/inventory');
}

export async function getAnomalies() {
  return fetchAPI('/anomalies');
}

export async function getShipmentDelays() {
  return fetchAPI('/shipments/delays');
}

export async function getSupplierScores() {
  return fetchAPI('/suppliers/scores');
}

export async function getRecommendations() {
  return fetchAPI('/recommendations');
}

export async function getAllocationPriority(productId: string = 'p1') {
  return fetchAPI(`/allocation/${productId}`);
}

export async function getProcurementSuggestions() {
  return fetchAPI('/procurement/suggestions');
}

export async function triggerDemoDelay() {
  return fetchAPI('/simulate/trigger-delay', { method: 'POST' });
}

export async function sendChatQuery(query: string, conversationId?: string) {
  return fetchAPI('/chat/query', {
    method: 'POST',
    body: JSON.stringify({ 
      user_query: query,
      conversation_id: conversationId || "default_session"
    })
  });
}
