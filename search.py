from util import spearman, kendal_tau


def main():
    #rank1 = [1,2,3,4,5,6,7,8,9,10]
    #rank2 = [3,1,2,5,4,9,6,7,10,8]
    rank1 = [1,2,3,4,5]
    rank2 = [3,1,2,5,4]
    return kendal_tau(rank1,rank2)


if __name__ == "__main__":
    print(main())