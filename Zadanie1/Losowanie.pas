program GenerateAndSort;
uses crt;

var 
    numbers: array[1..50] of integer;
    i: integer;

procedure generateNumbers;
    var k: integer;
begin
    randomize;
    for k := 1 to 50 do
    begin
        numbers[k]:= random(101)
    end;
end;

procedure bubbleSort;
var
  j, temp: integer;
  swapped: boolean;
begin
  for i := 1 to 49 do
  begin
    swapped := false;
    for j := 1 to 50 - i do
    begin
      if numbers[j] > numbers[j + 1] then
      begin
        temp := numbers[j];
        numbers[j] := numbers[j + 1];
        numbers[j + 1] := temp;
        swapped := true;
      end;
    end;
    if not swapped then break;
  end;
end;

begin

    generateNumbers;
    writeln('Unsorted numbers: ');

    for i := 1 to 50 do
    begin
        write(numbers[i], ' ');
        if i mod 10 = 0 then writeln;
    end;

    bubbleSort;
    writeln('Sorted numbers: ');

    for i := 1 to 50 do
    begin
        write(numbers[i], ' ');
        if i mod 10 = 0 then writeln;
    end;

end.