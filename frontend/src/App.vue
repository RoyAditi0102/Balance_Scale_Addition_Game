<script setup>
import { ref, onMounted, computed } from "vue";
import api from "./api.js";

// 🎬 Entry screen toggle
const showEntry = ref(true);
const startGame = () => {
  console.log("clicked!");
  showEntry.value = false;
};

// Game state
const numbers = ref([]);
const selectedNumbers = ref([]);
const sum = ref(0);
const target = ref(0);
const statusMessage = ref("");
const scaleTilt = ref("balanced");

// Target visual breakdown
const targetVisuals = computed(() => {
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

// Backend calls
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
    triggerStatusPop("Failed to load game!");
  }
};
 const showWinPopup = ref(false);
 
const selectNumber = async (num) => {
  try {
    const response = await api.post("/select-number", { num });
    sum.value = response.data.sum;
    selectedNumbers.value = response.data.selected_numbers;
    triggerStatusPopup(response.data.status);
    updateScaleTilt();

    if (response.data.status === "Correct! You matched the target.") {
      showWinPopup.value = true;
    }
  } catch (error) {
    console.error("Error selecting number", error);
    triggerStatusPopup("Failed to update selection!");
  }
};

const resetGame = async () => {
  try {
    const response = await api.post("/reset-game");
    numbers.value = response.data.numbers;
    sum.value = 0;
    selectedNumbers.value = [];
    target.value = response.data.target;
    triggerStatusPopup("Game Reset!");
    scaleTilt.value = "balanced"; 
  } catch (error) {
    console.error("Error resetting game:", error);
    triggerStatusPopup("Failed to reset game!");
  }
};

const updateScaleTilt = () => {
  if (sum.value < target.value) {
    scaleTilt.value = "left";
  } else if (sum.value > target.value) {
    scaleTilt.value = "right";
  } else {
    scaleTilt.value = "balanced";
  }
};

const tiltAngle = computed(() => {
  const diff = sum.value - target.value; 
  return Math.max(Math.min(diff * 2, 30), -30);
});

const clearLastNumber = async () => {
  try {
    const response = await api.post("/undo-last");
    sum.value = response.data.sum;
    selectedNumbers.value = response.data.selected_numbers;
    statusMessage.value = response.data.status;
    updateScaleTilt();

    if (response.data.status === "Correct! You matched the target.") {
      showWinPopup.value = true;
    } else {
      showWinPopup.value = false;
    }
  } catch (error) {
    console.error("Error undoing last number:", error);
    triggerStatusPopup("Failed to undo last number!");
  }
};

const resetWithPopupClose = () => {
  showWinPopup.value = false;
  resetGame();
};

const showStatusPopup = ref(false);

const triggerStatusPopup = (message) => {
  statusMessage.value = message;
  showStatusPopup.value = true;
  setTimeout(() => {
    showStatusPopup.value = false;
  }, 2000); // Hide after 2 seconds
};

onMounted(fetchGameState);
</script>


<template>
  <div class="background-wrapper">
    <!-- Background Image -->
    <div class="background-image"></div>

    <!-- Entry Screen -->
    <transition name="fade-scale">
      <div class="entry-screen" v-if="showEntry">
        <button class="start-button" @click="startGame">Start Game</button>
      </div>
    </transition>

    <!-- Game Section -->
    <transition name="fade-scale">
      <div class="game-overlay" v-if="!showEntry">
        <div class="game-container">
          <div class="target-card text-right">
            Target Sum : {{ target }}
          </div>
          <transition name="fade-popup">
  <div v-if="showStatusPopup" class="status-toast">
    {{ statusMessage }}
  </div>
</transition>

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
    :cy="80 - tiltAngle / 2 - 20 - idx * 12"
    r="8"
    fill="#fcd5ce"
    stroke="#333"
  />
  <text
    :x="60"
    :y="80 - tiltAngle / 2 - 20 - idx * 12 + 3"
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
    :cy="80 + tiltAngle / 2 - 20 - index * 12"
    r="8"
    fill="#d4f1f4"
    stroke="#333"
  />
  <text
    :x="140"
    :y="80 + tiltAngle / 2 - 20 - index * 12 + 3"
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
              :class="{ 'disabled-number': selectedNumbers.includes(num) }"
            >
              {{ num }}
            </button>
          </div>

          <div
  class="sum-card selected-card"
  :class="{
    'under': sum < target,
    'over': sum > target,
    'matched': sum === target
  }"
>
  Selected Sum: <span>{{ sum }}</span>
</div>

          <!-- Action buttons -->
<div class="actions">
  <button @click="resetGame">Reset</button>
  <button @click="clearLastNumber" :disabled="selectedNumbers.length === 0" class="clear-button">
    Clear Last
  </button>
  </div>

  <transition name="fade-popup">
  <div v-if="showWinPopup" class="win-popup-overlay">
    <div class="win-popup">
      <h2> You Matched the Target! 🎯</h2>
      <p>Great job, keep practicing!</p>
      <button @click="resetWithPopupClose">Play Again</button>
    </div>
  </div>
</transition>

        </div>
      </div>
    </transition>
  </div>
</template>

<style src="./assets/style.css"></style>
