python3 Map.py
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
   echo "This is a Linux operating system."
   firefox Visualize.html
else 
    @echo "Assuming this is opening in Mac"
    open -a /Applications/Firefox.app Visualize.html

fi
