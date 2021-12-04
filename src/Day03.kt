import java.io.File

fun main() {
    val size = 12
    val diffs = IntArray(size)
    val values: MutableList<CharArray> = arrayListOf()
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

    val oxygen = decode(determineRating(values, true))
    val co2 = decode(determineRating(values, false))
    print("Part Two: ")
    print(oxygen)
    print('x')
    print(co2)
    print('=')
    println(oxygen * co2)
}

private fun getMostCommon(
    values: List<CharArray>,
    position: Int
): Char {
    var diff = 0
    for (value in values)
        if (value[position] == '1')
            diff++
        else
            diff--
    if (diff >= 0)
        return '1'
    else
        return '0'
}

private fun selectValues(
    values: List<CharArray>,
    position: Int,
    key: Char
): List<CharArray> {
    val newValues: MutableList<CharArray> = arrayListOf()
    for (value in values)
        if (value[position] == key)
            newValues.add(value)
    return newValues
}

private fun determineRating(
    initialValues: List<CharArray>,
    mostCommon: Boolean
): CharArray {
    var position = 0
    var values = initialValues
    while (values.size > 1) {
        val common = getMostCommon(values, position)
        if (mostCommon)
            values = selectValues(values, position, common)
        else
            if (common == '1')
                values = selectValues(values, position, '0')
            else
                values = selectValues(values, position, '1')
        position++
    }
    return values[0]
}

private fun decode(
    code: CharArray
): Int {
    return Integer.parseInt(String(code), 2)
}

/*
val myValues: MutableList<CharArray> = arrayListOf()
myValues.add("00100".toCharArray())
myValues.add("11110".toCharArray())
myValues.add("10110".toCharArray())
myValues.add("10111".toCharArray())
myValues.add("10101".toCharArray())
myValues.add("01111".toCharArray())
myValues.add("00111".toCharArray())
myValues.add("11100".toCharArray())
myValues.add("10000".toCharArray())
myValues.add("11001".toCharArray())
myValues.add("00010".toCharArray())
myValues.add("01010".toCharArray())
*/
