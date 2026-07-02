import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getTodos } from '../api/client';
import { Todo } from '../api/client';

interface DashboardStats {
  totalTodos: number;
  completedTodos: number;
  pendingTodos: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentTodos, setRecentTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      setError(null);
      try {
        const todos = await getTodos();
        const totalTodos = todos.length;
        const completedTodos = todos.filter(todo => todo.completed).length;
        const pendingTodos = totalTodos - completedTodos;
        const recentTodos = todos.slice(0, 5);

        setStats({ totalTodos, completedTodos, pendingTodos });
        setRecentTodos(recentTodos);
      } catch (err) {
        setError('Failed to fetch dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleQuickAction = (action: string) => {
    if (action === 'addTodo') {
      navigate('/todos/new');
    } else if (action === 'viewTodos') {
      navigate('/todos');
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {loading && <p className="text-gray-600">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && !error && stats && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white shadow-md rounded-lg p-4">
              <h2 className="text-lg font-semibold">Total Todos</h2>
              <p className="text-2xl font-bold">{stats.totalTodos}</p>
            </div>
            <div className="bg-white shadow-md rounded-lg p-4">
              <h2 className="text-lg font-semibold">Completed Todos</h2>
              <p className="text-2xl font-bold">{stats.completedTodos}</p>
            </div>
            <div className="bg-white shadow-md rounded-lg p-4">
              <h2 className="text-lg font-semibold">Pending Todos</h2>
              <p className="text-2xl font-bold">{stats.pendingTodos}</p>
            </div>
          </div>
          <div className="mb-6">
            <h2 className="text-xl font-bold mb-4">Recent Todos</h2>
            <ul className="bg-white shadow-md rounded-lg divide-y divide-gray-200">
              {recentTodos.map(todo => (
                <li key={todo.id} className="p-4">
                  <p className="font-semibold">{todo.title}</p>
                  <p className="text-sm text-gray-600">{todo.completed ? 'Completed' : 'Pending'}</p>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
            <div className="flex space-x-4">
              <button
                onClick={() => handleQuickAction('addTodo')}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-blue-600"
              >
                Add Todo
              </button>
              <button
                onClick={() => handleQuickAction('viewTodos')}
                className="bg-green-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-green-600"
              >
                View Todos
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;