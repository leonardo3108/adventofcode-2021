import java.io.File

fun main() {
    var oldValue = 99999
    var countOne = 0
    var countThree = 0
    var last = 99999
    var penultimate = 99999
    var oldSigma = 99999
    File("resource/day01.txt").forEachLine {
        val newValue = it.toInt()
        val sigma = newValue + last + penultimate
        if (newValue > oldValue)
            countOne ++
        if ((sigma < 99999) && (sigma > oldSigma))
            countThree ++
        oldValue = newValue
        oldSigma = sigma
        penultimate = last
        last = newValue
    }
    print("Part One:")
    println(countOne)
    print("Part Two:")
    println(countThree)
}