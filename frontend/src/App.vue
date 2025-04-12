<script setup>
import { ref, onMounted, computed } from "vue";
import api from "./api.js";

const numbers = ref([]);
const selectedNumbers = ref([]);
const sum = ref(0);
const target = ref(0);
const statusMessage = ref("");
const scaleTilt = ref("balanced");

// Fetch game state from API
const fetchGameState = async () => {
  try {
    const response = await api.get("/game-state");
    numbers.value = response.data.numbers;
    sum.value = response.data.sum;
    target.value = response.data.target;
    selectedNumbers.value = response.data.selected_numbers;
    updateScaleTilt();
  } catch (error) {
    console.error("Error fetching game state:", error);
    statusMessage.value = "Failed to load game!";
  }
};

// Handle number selection
const selectNumber = async (num) => {
  try {
    const response = await api.post("/select-number", { num });
    sum.value = response.data.sum;
    selectedNumbers.value = response.data.selected_numbers;
    statusMessage.value = response.data.status;
    updateScaleTilt();
  } catch (error) {
    console.error("Error selecting number", error);
    statusMessage.value = "Failed to update selection!";
  }
};

// Reset game state
const resetGame = async () => {
  try {
    const response = await api.post("/reset-game");
    numbers.value = response.data.numbers;
    sum.value = 0;
    selectedNumbers.value = [];
    target.value = response.data.target;
    statusMessage.value = "Game Reset!";
    scaleTilt.value = "balanced"; 
  } catch (error) {
    console.error("Error resetting game:", error);
    statusMessage.value = "Failed to reset game!";
  }
};

// Update scale tilt based on sum difference
const updateScaleTilt = () => {
  if (sum.value < target.value) {
    scaleTilt.value = "left";
  } else if (sum.value > target.value) {
    scaleTilt.value = "right";
  } else {
    scaleTilt.value = "balanced";
  }
};

// Compute tilt angle dynamically
const tiltAngle = computed(() => {
  const diff = sum.value - target.value;
  return Math.max(Math.min(diff * 2, 30), -30); // Limit tilt between -30° to 30°
});

const targetVisuals = computed(() => {
  // For simplicity, break into approximate values
  const vals = [];
  let remaining = target.value;
  while (remaining >= 10) {
    vals.push(10);
    remaining -= 10;
  }
  if (remaining >= 5) {
    vals.push(5);
    remaining -= 5;
  }
  if (remaining > 0) {
    vals.push(remaining);
  }
  return vals;
});

</script>

<template>
  <div class="game-container">
    <h1>Balance Scale Addition</h1>
    <p>Target Sum: {{ target }}</p>

    <p class="status">{{ statusMessage }}</p>

<!-- Balance Scale -->
<div class="scale-container">
  <svg viewBox="0 0 200 100" class="balance-scale">
    <!-- Base -->
    <rect x="90" y="50" width="20" height="50" fill="black" />

    <!-- Beam -->
    <rect
      x="50"
      y="45"
      width="100"
      height="5"
      fill="black"
      :transform="`rotate(${tiltAngle} 100 50)`"
    />

    <!-- Left Pan - Target Weights -->
<g>
  <circle :cx="60" :cy="80 - tiltAngle / 2" r="15" fill="gray" />
  <g v-for="(n, idx) in targetVisuals" :key="'left-'+idx">
    <circle
      :cx="60"
      :cy="80 + tiltAngle / 2 - 20 - idx * 12"
      r="8"
      fill="#fcd5ce"
      stroke="#333"
    />
    <text
      :x="60"
      :y="80 + tiltAngle / 2 - 20 - idx * 12 + 3"
      text-anchor="middle"
      font-size="7"
      fill="#000"
    >
      {{ n }}
    </text>
  </g>
</g>

<!-- Right Pan - Selected Numbers -->
<g>
  <circle :cx="140" :cy="80 + tiltAngle / 2" r="15" fill="gray" />
  <g v-for="(num, index) in selectedNumbers" :key="'right-'+index">
    <circle
      :cx="140"
      :cy="80 - tiltAngle / 2 - 20 - index * 12"
      r="8"
      fill="#d4f1f4"
      stroke="#333"
    />
    <text
      :x="140"
      :y="80 - tiltAngle / 2 - 20 - index * 12 + 3"
      text-anchor="middle"
      font-size="7"
      fill="#000"
    >
      {{ num }}
    </text>
  </g>
</g>

  </svg>
</div>


    <!-- Number Buttons -->
    <div class="numbers">
      <button 
        v-for="num in numbers" 
        :key="num" 
        @click="selectNumber(num)" 
        :disabled="selectedNumbers.includes(num)"
      >
        {{ num }}
      </button>
    </div>

    <p>Selected Sum: {{ sum }}</p>

    <button @click="resetGame">Reset</button>
  </div>
</template>

<style src="./assets/style.css"></style>
