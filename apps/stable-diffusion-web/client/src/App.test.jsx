import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import axios from "axios";
import App from "./App.jsx";

vi.mock("axios", () => ({ default: { get: vi.fn() } }));
beforeEach(() => {
  URL.createObjectURL = vi.fn(() => "blob:generated");
  URL.revokeObjectURL = vi.fn();
  Object.defineProperty(window, "matchMedia", { writable: true, value: vi.fn(() => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() {} })) });
});
afterEach(() => { cleanup(); vi.clearAllMocks(); });

describe("Stable Diffusion client", () => {
  it("does not send a blank prompt", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: "Generate" }).disabled).toBe(true);
    expect(axios.get).not.toHaveBeenCalled();
  });
  it("encodes special characters as query parameters and displays the PNG blob", async () => {
    axios.get.mockResolvedValue({ data: new Blob(["PNG"], { type: "image/png" }) });
    const view = render(<App />);
    fireEvent.change(screen.getByLabelText("Image prompt"), { target: { value: "  astronaut & horse # Mars?  " } });
    fireEvent.click(screen.getByRole("button", { name: "Generate" }));
    await waitFor(() => expect(URL.createObjectURL).toHaveBeenCalled());
    expect(axios.get).toHaveBeenCalledWith("http://127.0.0.1:8000/", { params: { prompt: "astronaut & horse # Mars?", seed: 1024 }, responseType: "blob" });
    await waitFor(() => expect(screen.getByRole("button", { name: "Generate" }).disabled).toBe(false));
    view.unmount();
    expect(URL.revokeObjectURL).toHaveBeenCalledWith("blob:generated");
  });
  it("shows failures and restores the generate button", async () => {
    axios.get.mockRejectedValue(new Error("offline"));
    render(<App />);
    fireEvent.change(screen.getByLabelText("Image prompt"), { target: { value: "horse" } });
    fireEvent.click(screen.getByRole("button", { name: "Generate" }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("generation failed"));
    expect(screen.getByRole("button", { name: "Generate" }).disabled).toBe(false);
  });
});
