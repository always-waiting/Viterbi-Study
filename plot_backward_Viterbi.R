mydata<-read.table('result_plot',header=F,sep="\t")
x<-mydata[,1]
y<-mydata[,2]
output<-'backward_Viterbi.pdf'
pdf(file=output)
plot(x,y,type="l")
dev.off()
