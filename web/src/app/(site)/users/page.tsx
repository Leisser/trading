"use client";

import React, { useState, useEffect } from 'react';
import { Icon } from "@iconify/react";
import { useRouter } from 'next/navigation';
import { apiEndpoint } from '@/config/api';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_superuser: boolean;
  is_staff: boolean;
  date_joined: string;
  last_login: string;
  total_balance_usd: number;
}

interface UsersResponse {
  users: User[];
  total_count: number;
  total_balance_usd: number;
}

export default function UsersPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<User[]>([]);
  const [totalBalance, setTotalBalance] = useState(0);
  const [isAdmin, setIsAdmin] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'email' | 'balance' | 'date_joined'>('email');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    checkAdminAccess();
  }, []);

  const checkAdminAccess = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/signin');
        return;
      }

      const response = await fetch(apiEndpoint('/api/admin/users/'), {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        setIsAdmin(true);
        loadUsersData();
      } else {
        console.error('Access denied - not an admin user');
        router.push('/board');
      }
    } catch (error) {
      console.error('Failed to check admin access:', error);
      router.push('/board');
    }
  };

  const loadUsersData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      const response = await fetch(apiEndpoint('/api/admin/users/'), {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      
      if (response.ok) {
        const data: UsersResponse = await response.json();
        setUsers(data.users || []);
        setTotalBalance(data.total_balance_usd || 0);
      } else {
        console.error('Failed to load users data');
      }
    } catch (error) {
      console.error('Failed to load users data:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredAndSortedUsers = users
    .filter(user => 
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      `${user.first_name} ${user.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      let aValue: string | number;
      let bValue: string | number;

      switch (sortBy) {
        case 'balance':
          aValue = a.total_balance_usd;
          bValue = b.total_balance_usd;
          break;
        case 'date_joined':
          aValue = new Date(a.date_joined).getTime();
          bValue = new Date(b.date_joined).getTime();
          break;
        default:
          aValue = a.email.toLowerCase();
          bValue = b.email.toLowerCase();
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-darkmode pt-32 pb-16">
        <div className="container mx-auto max-w-7xl px-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <p className="text-white mt-4">Loading users...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-darkmode pt-32 pb-16">
      <div className="container mx-auto max-w-7xl px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-white text-4xl font-bold mb-2">Users Management</h1>
            <p className="text-muted text-lg">Manage all users in the system</p>
          </div>
          <button
            onClick={() => router.push('/board')}
            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-opacity-90 transition-all flex items-center gap-2"
          >
            <Icon icon="tabler:arrow-left" width="20" height="20" />
            Back to Board
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-muted text-sm">Total Users</p>
                <p className="text-white text-2xl font-bold">{users.length}</p>
              </div>
              <Icon icon="tabler:users" width="32" height="32" className="text-primary" />
            </div>
          </div>
          
          <div className="bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-muted text-sm">Active Users</p>
                <p className="text-white text-2xl font-bold">
                  {users.filter(user => user.is_active).length}
                </p>
              </div>
              <Icon icon="tabler:user-check" width="32" height="32" className="text-success" />
            </div>
          </div>
          
          <div className="bg-dark_grey rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-muted text-sm">Total Balance</p>
                <p className="text-white text-2xl font-bold">{formatCurrency(totalBalance)}</p>
              </div>
              <Icon icon="tabler:wallet" width="32" height="32" className="text-warning" />
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-dark_grey rounded-lg p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Icon 
                  icon="tabler:search" 
                  width="20" 
                  height="20" 
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted" 
                />
                <input
                  type="text"
                  placeholder="Search users by email or name..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-darkmode border border-dark_border rounded-lg pl-10 pr-4 py-3 text-white placeholder-muted focus:border-primary focus:outline-none"
                />
              </div>
            </div>
            
            <div className="flex gap-4">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'email' | 'balance' | 'date_joined')}
                className="bg-darkmode border border-dark_border rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
              >
                <option value="email">Sort by Email</option>
                <option value="balance">Sort by Balance</option>
                <option value="date_joined">Sort by Join Date</option>
              </select>
              
              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="bg-primary text-white px-4 py-3 rounded-lg hover:bg-opacity-90 transition-all flex items-center gap-2"
              >
                <Icon 
                  icon={sortOrder === 'asc' ? 'tabler:arrow-up' : 'tabler:arrow-down'} 
                  width="16" 
                  height="16" 
                />
                {sortOrder === 'asc' ? 'Asc' : 'Desc'}
              </button>
            </div>
          </div>
        </div>

        {/* Users Table */}
        <div className="bg-dark_grey rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-darkmode">
                <tr>
                  <th className="text-left p-4 text-white font-semibold">User</th>
                  <th className="text-left p-4 text-white font-semibold">Balance</th>
                  <th className="text-left p-4 text-white font-semibold">Status</th>
                  <th className="text-left p-4 text-white font-semibold">Roles</th>
                  <th className="text-left p-4 text-white font-semibold">Joined</th>
                  <th className="text-left p-4 text-white font-semibold">Last Login</th>
                  <th className="text-left p-4 text-white font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredAndSortedUsers.map((user) => (
                  <tr key={user.id} className="border-t border-dark_border hover:bg-darkmode hover:bg-opacity-50 transition-colors">
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-primary bg-opacity-20 rounded-full flex items-center justify-center">
                          <Icon icon="tabler:user" width="20" height="20" className="text-primary" />
                        </div>
                        <div>
                          <p className="text-white font-medium">
                            {user.first_name && user.last_name 
                              ? `${user.first_name} ${user.last_name}` 
                              : 'No Name'}
                          </p>
                          <p className="text-muted text-sm">{user.email}</p>
                        </div>
                      </div>
                    </td>
                    
                    <td className="p-4">
                      <p className="text-white font-semibold">
                        {formatCurrency(user.total_balance_usd)}
                      </p>
                    </td>
                    
                    <td className="p-4">
                      <span className={`px-3 py-1 rounded-full text-sm ${
                        user.is_active 
                          ? 'bg-success bg-opacity-20 text-success' 
                          : 'bg-error bg-opacity-20 text-error'
                      }`}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    
                    <td className="p-4">
                      <div className="flex gap-2">
                        {user.is_superuser && (
                          <span className="px-2 py-1 rounded-full text-xs bg-warning bg-opacity-20 text-warning">
                            Admin
                          </span>
                        )}
                        {user.is_staff && (
                          <span className="px-2 py-1 rounded-full text-xs bg-primary bg-opacity-20 text-primary">
                            Staff
                          </span>
                        )}
                        {!user.is_superuser && !user.is_staff && (
                          <span className="px-2 py-1 rounded-full text-xs bg-muted bg-opacity-20 text-muted">
                            User
                          </span>
                        )}
                      </div>
                    </td>
                    
                    <td className="p-4">
                      <p className="text-white text-sm">{formatDate(user.date_joined)}</p>
                    </td>
                    
                    <td className="p-4">
                      <p className="text-white text-sm">
                        {user.last_login ? formatDate(user.last_login) : 'Never'}
                      </p>
                    </td>
                    
                    <td className="p-4">
                      <div className="flex gap-2">
                        <button className="bg-primary text-white px-3 py-1 rounded text-sm hover:bg-opacity-90 transition-all flex items-center gap-1">
                          <Icon icon="tabler:eye" width="14" height="14" />
                          View
                        </button>
                        <button className="bg-warning text-white px-3 py-1 rounded text-sm hover:bg-opacity-90 transition-all flex items-center gap-1">
                          <Icon icon="tabler:edit" width="14" height="14" />
                          Edit
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Empty State */}
        {filteredAndSortedUsers.length === 0 && (
          <div className="text-center py-12">
            <Icon icon="tabler:users-off" width="64" height="64" className="text-muted mx-auto mb-4" />
            <p className="text-muted text-lg">No users found</p>
            <p className="text-muted text-sm">Try adjusting your search criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}
