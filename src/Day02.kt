import java.io.File
import kotlin.system.exitProcess

fun main() {
    var position = 0
    var depth = 0
    var depth2 = 0
    var aim = 0
    File("resource/input02.txt").forEachLine {
        val line = it.split(" ")
        val value = line[1].toInt()
        when (line[0]) {
            "forward" -> {
                position += value
                depth2 += aim * value
            }
            "down" -> {
                depth += value
                aim += value
            }
            "up" -> {
                depth -= value
                aim -= value
            }
            else -> {
                print(line)
                exitProcess(1)
            }
        }
    }
    print("Part One: ")
    print(position)
    print(" x ")
    print(depth)
    print(" = ")
    println(position * depth)
    print("Part Two: ")
    print(position)
    print(" x ")
    print(depth2)
    print(" = ")
    println(position * depth2)
}