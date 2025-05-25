import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics for MABOS performance testing
const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');
const workflowCreationTime = new Trend('workflow_creation_time');
const agentResponseTime = new Trend('agent_response_time');

// Test configuration for load testing
export const options = {
  stages: [
    // Ramp-up phase
    { duration: '2m', target: 10 },   // Ramp up to 10 users over 2 minutes
    { duration: '5m', target: 50 },   // Stay at 50 users for 5 minutes
    { duration: '5m', target: 100 },  // Ramp up to 100 users over 5 minutes
    { duration: '10m', target: 100 }, // Stay at 100 users for 10 minutes
    { duration: '5m', target: 200 },  // Ramp up to 200 users over 5 minutes
    { duration: '10m', target: 200 }, // Stay at 200 users for 10 minutes
    { duration: '5m', target: 0 },    // Ramp down to 0 users over 5 minutes
  ],
  thresholds: {
    // Performance thresholds for MABOS
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
    http_req_failed: ['rate<0.05'],    // Error rate must be below 5%
    errors: ['rate<0.05'],             // Custom error rate below 5%
    response_time: ['p(95)<1500'],     // 95% of API responses under 1.5s
    workflow_creation_time: ['p(95)<3000'], // Workflow creation under 3s
    agent_response_time: ['p(95)<2500'],    // BDI agent responses under 2.5s
  },
};

// Base URL configuration
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';
const FRONTEND_URL = __ENV.FRONTEND_URL || 'http://localhost:3000';

// Test data for MABOS workflows
const testWorkflows = [
  {
    name: 'Customer Onboarding',
    description: 'Automated customer onboarding process',
    steps: [
      { type: 'form', name: 'collect_info' },
      { type: 'validation', name: 'verify_identity' },
      { type: 'notification', name: 'send_welcome' }
    ]
  },
  {
    name: 'Invoice Processing',
    description: 'Automated invoice processing workflow',
    steps: [
      { type: 'ocr', name: 'extract_data' },
      { type: 'validation', name: 'verify_amounts' },
      { type: 'approval', name: 'manager_approval' }
    ]
  },
  {
    name: 'Support Ticket Routing',
    description: 'Intelligent support ticket routing',
    steps: [
      { type: 'classification', name: 'categorize_ticket' },
      { type: 'assignment', name: 'route_to_agent' },
      { type: 'notification', name: 'notify_customer' }
    ]
  }
];

// Authentication helper
function authenticate() {
  const loginPayload = {
    username: 'test_user',
    password: 'test_password'
  };

  const response = http.post(`${BASE_URL}/auth/login`, JSON.stringify(loginPayload), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(response, {
    'authentication successful': (r) => r.status === 200,
    'auth token received': (r) => r.json('access_token') !== undefined,
  });

  return response.json('access_token');
}

// Main test scenario
export default function () {
  // Authenticate user
  const token = authenticate();
  
  if (!token) {
    errorRate.add(1);
    return;
  }

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  // Test 1: Health check
  const healthResponse = http.get(`${BASE_URL}/health`, { headers });
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 500ms': (r) => r.timings.duration < 500,
  });
  responseTime.add(healthResponse.timings.duration);

  sleep(1);

  // Test 2: Get user profile
  const profileResponse = http.get(`${BASE_URL}/api/v1/users/me`, { headers });
  check(profileResponse, {
    'profile fetch status is 200': (r) => r.status === 200,
    'profile has user data': (r) => r.json('id') !== undefined,
  });
  responseTime.add(profileResponse.timings.duration);

  sleep(1);

  // Test 3: List workflows
  const workflowsResponse = http.get(`${BASE_URL}/api/v1/workflows`, { headers });
  check(workflowsResponse, {
    'workflows list status is 200': (r) => r.status === 200,
    'workflows list is array': (r) => Array.isArray(r.json()),
  });
  responseTime.add(workflowsResponse.timings.duration);

  sleep(1);

  // Test 4: Create new workflow
  const workflowData = testWorkflows[Math.floor(Math.random() * testWorkflows.length)];
  const createWorkflowResponse = http.post(
    `${BASE_URL}/api/v1/workflows`,
    JSON.stringify(workflowData),
    { headers }
  );
  
  check(createWorkflowResponse, {
    'workflow creation status is 201': (r) => r.status === 201,
    'workflow has ID': (r) => r.json('id') !== undefined,
  });
  workflowCreationTime.add(createWorkflowResponse.timings.duration);

  const workflowId = createWorkflowResponse.json('id');

  sleep(2);

  // Test 5: Execute workflow
  if (workflowId) {
    const executeResponse = http.post(
      `${BASE_URL}/api/v1/workflows/${workflowId}/execute`,
      JSON.stringify({ input_data: { test: true } }),
      { headers }
    );
    
    check(executeResponse, {
      'workflow execution status is 200': (r) => r.status === 200,
      'execution has result': (r) => r.json('execution_id') !== undefined,
    });
    responseTime.add(executeResponse.timings.duration);

    sleep(1);

    // Test 6: Check execution status
    const executionId = executeResponse.json('execution_id');
    if (executionId) {
      const statusResponse = http.get(
        `${BASE_URL}/api/v1/workflows/${workflowId}/executions/${executionId}`,
        { headers }
      );
      
      check(statusResponse, {
        'execution status check is 200': (r) => r.status === 200,
        'execution has status': (r) => r.json('status') !== undefined,
      });
      responseTime.add(statusResponse.timings.duration);
    }
  }

  sleep(1);

  // Test 7: BDI Agent interaction
  const agentQuery = {
    query: 'What is the status of my workflows?',
    context: { user_id: 'test_user' }
  };
  
  const agentResponse = http.post(
    `${BASE_URL}/api/v1/agents/query`,
    JSON.stringify(agentQuery),
    { headers }
  );
  
  check(agentResponse, {
    'agent query status is 200': (r) => r.status === 200,
    'agent provides response': (r) => r.json('response') !== undefined,
  });
  agentResponseTime.add(agentResponse.timings.duration);

  sleep(1);

  // Test 8: Enterprise integration status
  const integrationsResponse = http.get(`${BASE_URL}/api/v1/integrations`, { headers });
  check(integrationsResponse, {
    'integrations status is 200': (r) => r.status === 200,
    'integrations list exists': (r) => r.json() !== undefined,
  });
  responseTime.add(integrationsResponse.timings.duration);

  sleep(1);

  // Test 9: Analytics dashboard data
  const analyticsResponse = http.get(`${BASE_URL}/api/v1/analytics/dashboard`, { headers });
  check(analyticsResponse, {
    'analytics status is 200': (r) => r.status === 200,
    'analytics has metrics': (r) => r.json('metrics') !== undefined,
  });
  responseTime.add(analyticsResponse.timings.duration);

  sleep(1);

  // Test 10: WebSocket connection simulation
  const wsTestResponse = http.get(`${BASE_URL}/api/v1/ws/test`, { headers });
  check(wsTestResponse, {
    'websocket test status is 200': (r) => r.status === 200,
  });
  responseTime.add(wsTestResponse.timings.duration);

  // Random sleep between 1-3 seconds to simulate user behavior
  sleep(Math.random() * 2 + 1);
}

// Setup function - runs once before the test
export function setup() {
  console.log('Starting MABOS load test...');
  console.log(`Target URL: ${BASE_URL}`);
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  
  // Verify services are running
  const healthCheck = http.get(`${BASE_URL}/health`);
  if (healthCheck.status !== 200) {
    throw new Error('Backend service is not available');
  }
  
  console.log('Services are healthy, starting load test...');
}

// Teardown function - runs once after the test
export function teardown() {
  console.log('Load test completed');
  console.log('Check the results for performance metrics and thresholds');
} 