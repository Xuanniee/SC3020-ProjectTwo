import React from "react";
import { Input, VStack, Button, Text } from "@chakra-ui/react";

export default function InputBox({ textualPlaceholder, headerTitle, buttonText }) {
  return (
    <VStack flex="1">
        <Text>{headerTitle}</Text>
        <Input
            as="textarea"
            placeholder={textualPlaceholder}
            size="lg"
            variant="outline"
            minHeight="200px"
            width="100%"
            resize="vertical"
        />
        <Button>{buttonText}</Button>
    </VStack>
  );
}
