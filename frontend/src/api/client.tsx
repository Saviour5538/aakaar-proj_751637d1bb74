import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
}

export interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTodoRequest {
  title: string;
  description: string;
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface IngestDocumentsRequest {
  file: File;
  session_id: string;
  user_id: string;
}

export interface QueryRequest {
  query: string;
  session_id: string;
  user_id: string;
}

export interface QueryResponse {
  answer: string;
  sources: string[];
}

export const login = (data: LoginRequest) => api.post<TokenResponse>('/api/auth/login', data);

export const register = (data: RegisterRequest) => api.post('/api/auth/register', data);

export const listTodos = () => api.get<Todo[]>('/api/todos');

export const createTodo = (data: CreateTodoRequest) => api.post<Todo>('/api/todos', data);

export const getTodo = (id: number) => api.get<Todo>(`/api/todos/${id}`);

export const updateTodo = (id: number, data: UpdateTodoRequest) => api.put<Todo>(`/api/todos/${id}`, data);

export const toggleTodo = (id: number) => api.patch<Todo>(`/api/todos/${id}`);

export const deleteTodo = (id: number) => api.delete<void>(`/api/todos/${id}`);

export const ingestDocuments = (data: IngestDocumentsRequest) => {
  const formData = new FormData();
  formData.append('file', data.file);
  formData.append('session_id', data.session_id);
  formData.append('user_id', data.user_id);
  return api.post('/api/ai/ingest', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const aiQuery = (data: QueryRequest) => api.post<QueryResponse>('/api/ai/query', data);