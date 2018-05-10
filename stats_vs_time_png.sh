#==========================================================#
# Hashmi’s GNU Plot Script to Make Beautiful 2D Graphs.    #
#==========================================================#
#!/usr/local/bin/gnuplot
reset

#------------------------------------#
#  Set the terminal and fonts below  #
#------------------------------------#
set terminal png size 2420,1512 enhanced font "Arial,28" transparent  # Define the terminal, image size etc.
set encoding utf8 #iso_8859_1
set output 'output.png' # Define the output plot image.

#---------------#
#  Canvas style #
#---------------#
set border linewidth 2
### Set margins ###
set lmargin at screen 0.10
set rmargin at screen 0.97
set tmargin at screen  0.90
set bmargin at screen  0.25
#-------------------------------------------#
#  Set the Axis and Axis-Labels Formatting  #
#-------------------------------------------#
set format '%g'
#set title "A title can be added to the plot here" font "Arial,30" textcolor rgbcolor "#000000"

### Set x-axis data type
set xdata time
set timefmt '"%Y-%m-%d %H:%M:%S"'
set format x '"%Y-%m-%d %H:%M:%S"'

### Set xtics below ###
set xtics font "Arial,20" offset -7,-5 scale 3 # Font for xtics
set xtics mirror in rotate by 45 autojustify # Mirror/Show the small lines on the opposite side of the graph to make it easy to read from right side as well

### Set ytics below ###
set ytics font "Arial,20" scale 3
set ytics mirror in # Mirror/Show the small lines on the opposite side of the graph to make it easy to read from right side as well

### Set label for x-axis below ###
set xlabel font "Arial,40"
set xlabel 'Time Series' offset -1,-5 
set xrange [*:*] # Set the range for X-axis

### Set label for y-axis below ###
set ylabel font "Arial,40"
set ylabel offset -1,1 'Entropy' # Move ylabel 2 points towards x-axis, 0 points to y, and 0 points to z-axis
set yrange [*:*] # Set the range for Y-axis

#-------------------------------------------#
#  Set the Line Styles and Plot Formatting  #
#-------------------------------------------#
set style line 1 linecolor rgb '#0060ad' linetype 1 linewidth 5 pointtype 13 pointsize 4 # blue
set style line 2 lc rgb '#dd181f' lt 1 lw 5 pt 2 ps 3   # red
set style line 3 lc rgb '#1b7e2d' lt 1 lw 5 pt 57 ps 3   # green
set style line 4 lc rgb 'black' lt 1 lw 5 pt 149 ps 3 # black
set style line 5 lc rgb '#8B008B' lt 1 lw 5 pt 28 ps 3 # magenta


#===========================================#
# Plot the graph below.                     #
#===========================================#
#===============================================================================#
plot "output.txt" using 1:2 w lp ls 1 notitle


#=====================#
# Key for Some Terms  #
#=====================#
# lw = linewidth
# ls = linestyle
# lc = linecolor
# lp = linepoints
# pt = pointtype
# ps = pointsize
# w = with




