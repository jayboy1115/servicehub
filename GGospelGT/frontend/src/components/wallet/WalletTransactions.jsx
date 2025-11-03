import React, { useState, useEffect } from 'react';
import { walletAPI } from '../../api/wallet';
import { useToast } from '../../hooks/use-toast';

const WalletTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({ skip: 0, limit: 10 });
  const { toast } = useToast();

  useEffect(() => {
    fetchTransactions();
  }, [pagination.skip]);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const data = await walletAPI.getTransactions(pagination.skip, pagination.limit);
      setTransactions(data.transactions || []);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
      toast({
        title: "Error",
        description: "Failed to load transaction history",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const getTransactionIcon = (type) => {
    switch (type) {
      case 'wallet_funding':
        return <span className="text-green-600">+</span>;
      case 'access_fee_deduction':
        return <span className="text-red-600">-</span>;
      case 'refund':
        return <span className="text-blue-600">↺</span>;
      default:
        return <span className="text-gray-600">?</span>;
    }
  };

  const getStatusBadge = (status) => {
    const styles = {
      confirmed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      rejected: 'bg-red-100 text-red-800'
    };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-white p-4 rounded-lg shadow-sm border animate-pulse">
            <div className="flex justify-between items-center">
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 rounded w-32"></div>
                <div className="h-3 bg-gray-200 rounded w-24"></div>
              </div>
              <div className="h-6 bg-gray-200 rounded w-20"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-800">Transaction History</h3>
        <button
          onClick={fetchTransactions}
          className="text-blue-600 hover:text-blue-700 text-sm"
        >
          Refresh
        </button>
      </div>

      {transactions.length === 0 ? (
        <div className="bg-white p-8 rounded-lg shadow-sm border text-center">
          <div className="text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <p className="text-gray-600">No transactions yet</p>
          <p className="text-sm text-gray-500 mt-1">Your wallet transactions will appear here</p>
        </div>
      ) : (
        <div className="space-y-3">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="bg-white p-4 rounded-lg shadow-sm border hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex items-start space-x-3">
                  <div className="text-2xl">
                    {getTransactionIcon(transaction.transaction_type)}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-800">
                      {transaction.description}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {formatDate(transaction.created_at)}
                    </p>
                    {transaction.reference && (
                      <p className="text-xs text-gray-500 mt-1">
                        Ref: {transaction.reference}
                      </p>
                    )}
                    {transaction.admin_notes && (
                      <p className="text-xs text-blue-600 mt-1">
                        Note: {transaction.admin_notes}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={`font-semibold ${
                      transaction.transaction_type === 'wallet_funding' 
                        ? 'text-green-600' 
                        : 'text-red-600'
                    }`}>
                      {transaction.transaction_type === 'wallet_funding' ? '+' : '-'}
                      {transaction.amount_coins} coins
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 mb-2">
                    ₦{transaction.amount_naira.toLocaleString()}
                  </div>
                  {getStatusBadge(transaction.status)}
                </div>
              </div>
              
              {transaction.proof_image && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <p className="text-xs text-gray-500 mb-2">Payment Proof:</p>
                  <img
                    src={walletAPI.getPaymentProofUrl(transaction.proof_image)}
                    alt="Payment proof"
                    className="h-20 w-auto rounded border cursor-pointer hover:shadow-lg transition-shadow"
                    onClick={() => window.open(walletAPI.getPaymentProofUrl(transaction.proof_image), '_blank')}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {transactions.length === pagination.limit && (
        <div className="flex justify-center">
          <button
            onClick={() => setPagination(prev => ({ ...prev, skip: prev.skip + prev.limit }))}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            Load More
          </button>
        </div>
      )}
    </div>
  );
};

export default WalletTransactions;