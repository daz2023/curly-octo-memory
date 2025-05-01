import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardHeader,
  CardBody,
  Heading,
  Text,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  SimpleGrid,
  useColorModeValue,
} from '@chakra-ui/react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [marketData, setMarketData] = useState([]);
  const [portfolioValue, setPortfolioValue] = useState(0);
  const [performance, setPerformance] = useState({});

  useEffect(() => {
    // Fetch market data
    fetch('/api/market-data?symbols=AAPL,MSFT,GOOGL')
      .then(res => res.json())
      .then(data => {
        // Process data for chart
        const chartData = Object.entries(data).map(([symbol, df]) => ({
          date: df.index,
          [symbol]: df.Close
        }));
        setMarketData(chartData);
      });

    // Fetch portfolio value
    fetch('/api/portfolio')
      .then(res => res.json())
      .then(data => {
        setPortfolioValue(data.portfolio_value);
      });

    // Fetch performance metrics
    fetch('/api/performance')
      .then(res => res.json())
      .then(data => {
        setPerformance(data.metrics);
      });
  }, []);

  const cardBg = useColorModeValue('white', 'gray.700');

  return (
    <Box>
      <Heading mb={6}>Dashboard</Heading>
      
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={6}>
        <Card bg={cardBg}>
          <CardBody>
            <Stat>
              <StatLabel>Portfolio Value</StatLabel>
              <StatNumber>${portfolioValue.toLocaleString()}</StatNumber>
              <StatHelpText>Current Value</StatHelpText>
            </Stat>
          </CardBody>
        </Card>

        <Card bg={cardBg}>
          <CardBody>
            <Stat>
              <StatLabel>Win Rate</StatLabel>
              <StatNumber>{performance.win_rate?.toFixed(2)}%</StatNumber>
              <StatHelpText>All Time</StatHelpText>
            </Stat>
          </CardBody>
        </Card>

        <Card bg={cardBg}>
          <CardBody>
            <Stat>
              <StatLabel>Total Trades</StatLabel>
              <StatNumber>{performance.total_trades}</StatNumber>
              <StatHelpText>All Time</StatHelpText>
            </Stat>
          </CardBody>
        </Card>
      </SimpleGrid>

      <Card bg={cardBg} mb={6}>
        <CardHeader>
          <Heading size="md">Market Overview</Heading>
        </CardHeader>
        <CardBody>
          <Box h="400px">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={marketData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="AAPL" stroke="#8884d8" />
                <Line type="monotone" dataKey="MSFT" stroke="#82ca9d" />
                <Line type="monotone" dataKey="GOOGL" stroke="#ffc658" />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        </CardBody>
      </Card>

      <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={6}>
        <Card bg={cardBg}>
          <CardHeader>
            <Heading size="md">Recent Trades</Heading>
          </CardHeader>
          <CardBody>
            {/* Add recent trades list here */}
          </CardBody>
        </Card>

        <Card bg={cardBg}>
          <CardHeader>
            <Heading size="md">Active Positions</Heading>
          </CardHeader>
          <CardBody>
            {/* Add active positions list here */}
          </CardBody>
        </Card>
      </Grid>
    </Box>
  );
}

export default Dashboard; 