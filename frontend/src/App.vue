<script setup>
import { ref, onMounted } from "vue";
import api from "./api.js";

const numbers = ref([]);
const selectedNumbers = ref([]);
const sum = ref(0);
const target = ref(0);
const statusMessage = ref("");
const scaleTilt = ref("balanced");

const fetchGameState = async () => {
  try
  {
    const response = await api.get("/game-state");
    numbers.value = response.data.numbers;
    sum.value = response.data.sum;
    target.value = response.data.target;
    selectedNumbers.value = response.data.selected_numbers;
    updateScaleTilt();
  }
  catch(error){
    console.error("Error fetching game state:", error);
    statusMessage.value = "Failed to load game!";
  }
};

const selectNumber = async (num) => {
  try
  {
    const response = await api.post("/select-number", { num });
    sum.value = response.data.sum;
    selectedNumbers.value = response.data.selected_numbers;
    statusMessage.value = response.data.status;
    updateScaleTilt();
  }
  catch(error)
  {
    console.error("Error selecting number",error);
    statusMessage.value = "Failed to update selection!";
  }
};

const resetGame = async() => {
  try
  {
    const response = await api.post ("/reset-game");
    numbers.value = response.data.numbers;
    sum.value = 0;
    selectedNumbers.value = [];
    target.value = response.data.target;
    statusMessage.value = "Game Reset!";
    scaleTilt.value = "balanced"; 
  }
  catch(error)
  {
    console.error("Error resetting game:", error);
    statusMessage.value = "Failed to reset game!";
  }
};

const updateScaleTilt = () => {
  if (sum.value < target.value)
  {
    scaleTilt.value = "left";
  }
  else if (sum.value > target.value)
  {
    scaleTilt.value = "right";
  }
  else
  {
    scaleTilt.value = "balanced";
  }
};

onMounted(fetchGameState);
</script>

<template>
<div class = "game-container">
  <h1> Balance Scale Addition</h1>
  <p> Target Sum: {{ target }} </p>

  <div class = "scale" :class = "scaleTilt">
  <span v-if = "scaleTilt === 'left'">➘</span>
  <span v-if = "scaleTilt === 'right'">↙</span>
  <span v-if = "scaleTilt === 'balanced'">:)</span>
  </div>

  <div class = "numbers">
    <button v-for = "num in numbers" :key="num" @click = "selectNumber(num)" :disabled="selectedNumbers.includes(num)">
    {{ num }}
    </button>
  </div>

  <p>Selected Sum: {{ sum }}</p>
  <p class = "status">{{ statusMessage }} </p>

  <button @click = "resetGame"> Reset </button>
</div>  
</template>

<style src = "./assets/style.css"></style>
