python friedman.py eindex rus/t1.txt rus/t2.txt rus/alph.txt
python friedman.py eindex rus/t3.txt rus/t4.txt rus/alph.txt
python friedman.py eindex rus/t3.txt rus/t6.txt rus/alph.txt
python friedman.py eindex rus/t5.txt rus/t2.txt rus/alph.txt

python friedman.py meindex rus/t1.txt rus/t2.txt rus/alph.txt
python friedman.py meindex rus/t3.txt rus/t4.txt rus/alph.txt
python friedman.py meindex rus/t3.txt rus/t6.txt rus/alph.txt
python friedman.py meindex rus/t5.txt rus/t2.txt rus/alph.txt

python friedman.py eindex eng/t1.txt eng/t2.txt eng/alph.txt
python friedman.py eindex eng/t3.txt eng/t4.txt eng/alph.txt
python friedman.py eindex eng/t3.txt eng/t6.txt eng/alph.txt
python friedman.py eindex eng/t5.txt eng/t2.txt eng/alph.txt

python friedman.py meindex eng/t1.txt eng/t2.txt eng/alph.txt
python friedman.py meindex eng/t3.txt eng/t4.txt eng/alph.txt
python friedman.py meindex eng/t3.txt eng/t6.txt eng/alph.txt
python friedman.py meindex eng/t5.txt eng/t2.txt eng/alph.txt

python friedman.py gen rus/alph.txt 10000 seq1.txt
python friedman.py gen rus/alph.txt 10000 seq2.txt
python friedman.py gen rus/alph.txt 10000 seq3.txt
python friedman.py gen rus/alph.txt 10000 seq4.txt
python friedman.py gen eng/alph.txt 10000 seq5.txt
python friedman.py gen eng/alph.txt 10000 seq6.txt
python friedman.py gen eng/alph.txt 10000 seq7.txt
python friedman.py gen eng/alph.txt 10000 seq8.txt

python friedman.py eindex seq1.txt seq2.txt rus/alph.txt
python friedman.py eindex seq3.txt seq4.txt rus/alph.txt
python friedman.py eindex seq5.txt seq6.txt eng/alph.txt
python friedman.py eindex seq7.txt seq8.txt eng/alph.txt

python friedman.py meindex seq1.txt seq2.txt rus/alph.txt
python friedman.py meindex seq3.txt seq4.txt rus/alph.txt
python friedman.py meindex seq5.txt seq6.txt eng/alph.txt
python friedman.py meindex seq7.txt seq8.txt eng/alph.txt