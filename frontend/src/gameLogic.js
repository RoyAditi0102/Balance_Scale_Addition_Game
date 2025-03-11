import { ref } from "vue";

export function useGameLogic()
{
    const numbers = ref([1, 2, 3, 4, 5, 6, 7, 8, 9]);
    const selectedNumbers = ref([]);
    const sum = ref(0);
    const target = ref(10);
    const statusMessage = ref("");
    const scaleTilt = ref ("");

    function selectNumber(num)
    {
        if(!selectedNumbers.value.includes(num))
        {
            selectedNumbers.value.push(num);
            sum.value += num;

            if (sum.value === target.value)
                {
                    scaleTilt.value = "balanced";
                    statusMessage.value = "The scale is balanced";
                }
            else if (sum.value <target.value)
            {
                scaleTilt.value = "left";
                statusMessage.value = "";
            }
            else
            {
                scaleTilt.value = right;
                statusMessage.value = "Too much Weight!!!"
            }
        }
        
    }

    function resetGame()
    {
        selectedNumbers.value = [];
        sum.value = 0;
        scaleTilt.value = "";
        statusMessage.value = "";
    }

    return {
        numbers,
        selectedNumbers,
        sum,
        target,
        statusMessage,
        scaleTilt,
        selectNumber,
        resetGame,
    };
}