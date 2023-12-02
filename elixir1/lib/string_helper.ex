

defmodule StringHelper do

  defp find_occurrence_idcs(str, substr) do
    len = String.length(substr)
    Enum.filter(
      0..String.length(str),
      fn idx ->
	String.slice(str, idx, len) == substr
      end
    )
  end
  
  def findl(str, substr) do
    find_occurrence_idcs(str, substr)
    |> Enum.min(&<=/2, fn -> String.length(str) end)
  end

  def findr(str, substr) do
    find_occurrence_idcs(str, substr)
    |> Enum.max(&>=/2, fn -> -1 end)
  end

end
