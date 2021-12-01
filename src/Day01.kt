import java.io.File

fun main() {
    var oldValue = 99999
    var count = 0
    File("resource/day01.txt").forEachLine {
        val newValue = it.toInt()
        if (newValue > oldValue)
            count ++
        oldValue = newValue
    }
    print(count)
}
