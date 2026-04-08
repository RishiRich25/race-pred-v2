const API_BASE_URL = 'http://localhost:8000';

export const fetchNextRacePrediction = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict/next`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching next race prediction:', error);
    throw error;
  }
};

export const fetchRacePrediction = async (year, round) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict/race?year=${year}&round=${round}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching race prediction:', error);
    throw error;
  }
};

export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking API health:', error);
    throw error;
  }
};
