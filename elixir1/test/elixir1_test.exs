defmodule Elixir1Test do
  use ExUnit.Case


  test "findl prefix" do
    assert 0 == StringHelper.findl("abcdef", "abc")
  end

  test "findl middle" do
    assert 3 == StringHelper.findl("abcdef", "de")
  end

  test "findl end" do
    assert 3 == StringHelper.findl("abcde", "de")
  end

  test "find complete" do
    assert 0 == StringHelper.findl("abcde", "abcde")
  end

  test "find singleton" do
    assert 2 == StringHelper.findl("abcde", "c")
  end


  test "find multiple" do
    assert 2 == StringHelper.findl("abcdcdcdcdcdcd", "cd")
  end
  
  test "don't find in empty" do
    assert 0 == StringHelper.findl("", "abc")
  end

  test "don't find" do
    assert 5 == StringHelper.findl("abbca", "abc")
  end


  test "findr postfix" do
    assert 2 == StringHelper.findr("abcde", "cde")
  end

  test "findr middle" do
    assert 2 == StringHelper.findr("abcdef", "cde")
  end

  test "findr prefix" do
    assert 0 == StringHelper.findr("abcdef", "ab")
  end


  test "don't findr" do
    assert -1 == StringHelper.findr("abcdef", "abd")
  end 
  
  test "wrong line 1" do
    line = "zfssixvkhtlcmltwo7"
    assert 3 == StringHelper.findl(line, "six")
    assert 14 == StringHelper.findl(line, "two")
  end
end
