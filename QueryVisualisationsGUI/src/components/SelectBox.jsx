import React, { useState } from "react";
import { 
    Text, 
    Select, 
    VStack,  
    NumberInput,
    NumberInputField,
    NumberInputStepper,
    NumberIncrementStepper,
    NumberDecrementStepper, 
    Spacer, 
    Button,
    Box // Add the Box component
} from "@chakra-ui/react";

export default function SelectBox({ buttonText, questionPlaceholderText, stepPlaceholderText, headerText }) {
    const questionList = [
        "How many rows are left after a certain step?",
        "What are the operators used?",
        "What does an operator do?",
        "How long does it take to run a certain step?",
        "What is the most expensive step?",
        "What is the most inexpensive step?"
    ]

    // State to store options
    const [selectedQuestion, setSelectedQuestion] = useState("");

    // Handlers Functions
    const handleQuestionSelectChange = (event) => {
        setSelectedQuestion(event.target.value);
    };

    return (
        <>
            <VStack flex="1">
                <Text>{headerText}</Text>
                <Box // Use the Box component to wrap the content
                    p="4" // Padding
                    borderWidth="1px" // Border
                    borderColor="gray.300" // Border color
                    borderRadius="md" // Border radius
                    boxShadow="md" // Shadow
                    width="fit-content" // Fit content width
                >
                    <VStack spacing="4">
                        <Text>Question</Text>
                        <Select 
                            placeholder={questionPlaceholderText} 
                            variant="filled" // Style as filled input
                        >
                            {questionList.map((option, index) => (
                                <option key={index} value={option}>
                                    {option}
                                </option>
                            ))}
                        </Select>

                        <Text>Step</Text>
                        <NumberInput min={1} variant="filled">
                            <NumberInputField 
                                placeholder={stepPlaceholderText} 
                                _focus={{ borderColor: "teal.500" }} // Input field focus style
                            />
                            <NumberInputStepper>
                                <NumberIncrementStepper />
                                <NumberDecrementStepper />
                            </NumberInputStepper>
                        </NumberInput>

                        <Spacer />

                        <Button onClick={handleQuestionSelectChange} colorScheme="teal">
                            {buttonText}
                        </Button>
                    </VStack>
                </Box>
            </VStack>
        </>
    );
}
