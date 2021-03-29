
for filename in *.hs; do
    [ -e "$filename" ] || continue

    extension="${filename##*.}"
    
    binname=$(basename $filename .hs)
    echo $binname $extension
    # ... rest of the loop body
    ghc $filename -o build/$binname
done


