import React from 'react';
import { Box, Flex, Button, Heading, Spacer, useColorMode } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

function Navbar() {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Box bg="white" px={4} shadow="sm">
      <Flex h={16} alignItems="center" maxW="container.xl" mx="auto">
        <Heading size="md" color="blue.600">
          AI Hedge Fund
        </Heading>
        <Spacer />
        <Flex gap={4}>
          <Button as={RouterLink} to="/" variant="ghost">
            Dashboard
          </Button>
          <Button as={RouterLink} to="/portfolio" variant="ghost">
            Portfolio
          </Button>
          <Button as={RouterLink} to="/history" variant="ghost">
            History
          </Button>
          <Button as={RouterLink} to="/performance" variant="ghost">
            Performance
          </Button>
          <Button onClick={toggleColorMode} variant="ghost">
            {colorMode === 'light' ? '🌙' : '☀️'}
          </Button>
          <Button as={RouterLink} to="/login" colorScheme="blue">
            Login
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
}

export default Navbar; 