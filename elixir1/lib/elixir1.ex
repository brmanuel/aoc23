defmodule Elixir1 do
  @moduledoc """
  Documentation for `Elixir1`.
  """

  def solve1(filename) do
    numbers = %{
      "1" => 1,
      "2" => 2,
      "3" => 3,
      "4" => 4,
      "5" => 5,
      "6" => 6,
      "7" => 7,
      "8" => 8,
      "9" => 9
    }

    solve(filename, numbers)
    
  end


  def solve2(filename) do
    numbers = %{
      "1" => 1,
      "2" => 2,
      "3" => 3,
      "4" => 4,
      "5" => 5,
      "6" => 6,
      "7" => 7,
      "8" => 8,
      "9" => 9,
      "one" => 1,
      "two" => 2,
      "three" => 3,
      "four" => 4,
      "five" => 5,
      "six" => 6,
      "seven" => 7,
      "eight" => 8,
      "nine" => 9
    }

    solve(filename, numbers)
  end
  
  def solve(filename, numbers) do
    {:ok, contents} = File.read(filename)
    
    lines =
      contents
      |> String.split("\n", trim: true)

    left =
      lines
      |> Enum.map(&get_leftmost_in_line(&1, Map.keys(numbers)))
      |> Enum.map(&Map.get(numbers, &1))

    right =
      lines
      |> Enum.map(&get_rightmost_in_line(&1, Map.keys(numbers)))
      |> Enum.map(&Map.get(numbers, &1)) 

    
    left
    |> Enum.map(fn x -> 10*x end)
    |> Enum.concat(right)
    |> Enum.sum()

  end

  
  defp get_leftmost_in_line(line, candidates) do
    Enum.min(
      candidates,
      fn a,b -> StringHelper.findl(line, a) <= StringHelper.findl(line, b) end
    )
  end
  
  defp get_rightmost_in_line(line, candidates) do
    Enum.max(
      candidates,
      fn a,b -> StringHelper.findr(line, a) >= StringHelper.findr(line, b) end
    )
  end

  
  
  
end
