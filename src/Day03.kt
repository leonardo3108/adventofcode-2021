import java.io.File

fun main() {
    val size: Int = 12
    var diffs = IntArray(size)
    var values: MutableList<CharArray> = arrayListOf()
    File("resource/input03.txt").forEachLine {
        val newValue = it.toCharArray()
        values.add(newValue)
        for (pos in 0..size-1 ) {
            if (newValue[pos] == '1')
                diffs[pos]++
            else
                diffs[pos]--
        }
    }
    var gamma = 0
    var epsilon = 0
    for (pos in 0..size-1 )
        if (diffs[pos] > 0) {
            gamma = gamma * 2 + 1
            epsilon = epsilon * 2
        }
        else {
            gamma = gamma * 2
            epsilon = epsilon * 2 + 1
        }
    print("Part One: ")
    print(gamma)
    print('x')
    print(epsilon)
    print('=')
    println(gamma * epsilon)

    for (pos in 1..size-1 )
        diffs[pos] = 0
    var pos = 0
    val oxygen = determineRating(values, diffs, pos, size)
    val co2 = determineRating(values, diffs, pos, size, false)
    print("Part Two: ")
    print(oxygen)
    print('x')
    print(co2)
    print('=')
    println(oxygen * co2)
}

private fun determineRating(
    values: MutableList<CharArray>,
    diffs: IntArray,
    pos: Int,
    size: Int,
    mostCommon: Boolean = true
):Int {
    var values1 = values
    var pos1 = pos
    while (values1.size > 1) {
        var newValues: MutableList<CharArray> = arrayListOf()
        for (value in values1)
            if (mostCommon && (diffs[pos1] >= 0) != (value[pos1] == '1') || !mostCommon && (diffs[pos1] >= 0) == (value[pos1] == '1')) {
                newValues.add(value)
                if (pos1 < size - 1) {
                    if (value[pos1 + 1] == '1')
                        diffs[pos1 + 1]++
                    else
                        diffs[pos1 + 1]--
                }
            }
        pos1++
        values1 = newValues
    }
    var rating = 0
    if (values1.size == 1) {
        for (pos in 0..size - 1)
            if (values1[0][pos] == '1') {
                rating = rating * 2 + 1
            } else {
                rating = rating * 2
            }
    }
    return rating
}