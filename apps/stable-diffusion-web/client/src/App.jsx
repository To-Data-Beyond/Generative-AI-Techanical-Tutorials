import React, { useEffect, useState } from "react";
import { ChakraProvider, Container, Heading, Text, Input, Button, Image, Stack, Alert, AlertIcon, Skeleton } from "@chakra-ui/react";
import axios from "axios";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => () => { if (image) URL.revokeObjectURL(image); }, [image]);

  async function generate(event) {
    event.preventDefault();
    if (!prompt.trim() || loading) return;
    setLoading(true);
    setError("");
    try {
      const result = await axios.get("http://127.0.0.1:8000/", {
        params: { prompt: prompt.trim(), seed: 1024 }, responseType: "blob",
      });
      setImage(URL.createObjectURL(result.data));
    } catch {
      setError("Image generation failed. Please check the API and try again.");
    } finally {
      setLoading(false);
    }
  }

  return <ChakraProvider><Container maxW="2xl" py={10}>
    <Stack spacing={5}>
      <Heading>Stable Diffusion</Heading>
      <Text>Generate images with Stable Diffusion v1-4, FastAPI and React.</Text>
      <form onSubmit={generate}>
        <Input aria-label="Image prompt" value={prompt} maxLength={500} onChange={e => setPrompt(e.target.value)} placeholder="Describe your image" />
        <Button type="submit" mt={3} colorScheme="blue" isDisabled={!prompt.trim() || loading} isLoading={loading}>Generate</Button>
      </form>
      {error && <Alert status="error"><AlertIcon />{error}</Alert>}
      {loading ? <Skeleton height="256px" /> : image && <Image src={image} alt="Generated image" boxShadow="lg" />}
    </Stack>
  </Container></ChakraProvider>;
}
