import React from "react";
import { HStack, Spacer, VStack, Flex, Divider } from "@chakra-ui/react";

import NavBar from "../components/NavBar";
import InputBox from "../components/InputBox";
import SelectBox from "../components/SelectBox";

const containerStyle = {
  display: "flex",
  flexDirection: "column",
  height: "100%", // Define the height of the parent container
};

const rowStyle = {
  flex: "1", // Make the rows take up all available vertical space
};

export default function QueryGUI() {
  return (
    <div style={containerStyle}>
        <NavBar />
        <VStack style={rowStyle} spacing={4}>
            <HStack spacing={4} style={rowStyle}>
                <InputBox textualPlaceholder="Enter your SQL Query..." headerTitle="SQL Query" buttonText="Submit"/>
                <InputBox textualPlaceholder="Enter your SQL Query..." headerTitle="QEP Description" buttonText="Submit"/>
                <InputBox textualPlaceholder="Enter your SQL Query..." headerTitle="Visualize Plan" buttonText="Submit"/>
            </HStack>
        </VStack>

        <Spacer />

        <VStack style={rowStyle} spacing={4}>
            <HStack spacing={4} style={rowStyle}>
                <SelectBox buttonText="Submit" stepPlaceholderText="Provide the Step." questionPlaceholderText="Select a Question" headerText="Question"/>
                <InputBox textualPlaceholder="Enter your SQL Query..." headerTitle="Answer" buttonText="Submit"/>
                <InputBox textualPlaceholder="Please provide your feedback here..." headerTitle="Feedback" buttonText="Submit Feedback"/>
            </HStack>
        </VStack>
    </div>
  );
}
