import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface CommitInfo {
  id: string;
  message: string;
}

interface BranchInfo {
  name: string;
}

const VersionControlPanel: React.FC = () => {
  const [branches, setBranches] = useState<BranchInfo[]>([]);
  const [history, setHistory] = useState<CommitInfo[]>([]);
  const [commitMessage, setCommitMessage] = useState('');
  const [newBranchName, setNewBranchName] = useState('');

  useEffect(() => {
    fetchBranches();
    fetchHistory();
  }, []);

  const fetchBranches = async () => {
    const response = await axios.get('/api/v1/vc/branches');
    setBranches(response.data);
  };

  const fetchHistory = async () => {
    const response = await axios.get('/api/v1/vc/history');
    setHistory(response.data);
  };

  const handleCommit = async () => {
    await axios.post('/api/v1/vc/commit', { message: commitMessage });
    setCommitMessage('');
    fetchHistory();
  };

  const handleCreateBranch = async () => {
    await axios.post('/api/v1/vc/branch', { branch_name: newBranchName });
    setNewBranchName('');
    fetchBranches();
  };

  const handleMergeBranch = async (branchName: string) => {
    await axios.post('/api/v1/vc/merge', { branch_name: branchName });
    fetchBranches();
    fetchHistory();
  };

  return (
    <div>
      <h2>Version Control</h2>
      <div>
        <h3>Commit Changes</h3>
        <input 
          type="text" 
          value={commitMessage} 
          onChange={(e) => setCommitMessage(e.target.value)} 
          placeholder="Commit message"
        />
        <button onClick={handleCommit}>Commit</button>
      </div>
      <div>
        <h3>Create Branch</h3>
        <input 
          type="text" 
          value={newBranchName} 
          onChange={(e) => setNewBranchName(e.target.value)} 
          placeholder="New branch name"
        />
        <button onClick={handleCreateBranch}>Create Branch</button>
      </div>
      <div>
        <h3>Branches</h3>
        <ul>
          {branches.map((branch) => (
            <li key={branch.name}>
              {branch.name}
              <button onClick={() => handleMergeBranch(branch.name)}>Merge</button>
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Commit History</h3>
        <ul>
          {history.map((commit) => (
            <li key={commit.id}>{commit.message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default VersionControlPanel;