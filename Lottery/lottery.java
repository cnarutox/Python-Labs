import java.util.*;
public class LotteryTest {
	public static void main(String[] args) {
		LotteryTest a = new LotteryTest();
		int type; Lottery t = null;
		Scanner in = new Scanner(System.in);
		type = in.nextInt();
		switch(type)
		{
            case 1: t = a.new DoubleLottery(); break;
            case 2: t = a.new BigLottery(); break;
		}
		int input[] = new int[t.beforeCount + t.afterCount];
		for(int i = 0; i < input.length; i++)
			input[i] = in.nextInt();
		System.arraycopy(input, 0, t.beforenumber, 0, t.beforeCount);
		System.arraycopy(input, t.beforeCount, t.afternumber, 0, t.afterCount);
		if(!t.checkFormat(input))	
			System.out.println("ERROR");
		else System.out.println(t.getLevel(input));
		in.close(); 
	}
    abstract public class Lottery{
        int[] beforenumber;
        int[] afternumber;
        int[] winbnumber;
        int[] winanumber;
        int[] beforeRange = new int[2];
        int[] afterRange = new int[2];
        int beforeCount, afterCount;
        boolean checkFormat(int[] arg1)
        {	
            for(int i = 0; i < beforeCount + afterCount; i++)
                if(i < beforeCount && rightHere(arg1[i], beforeRange))
                    continue;
                else if(rightHere(arg1[i], afterRange)) continue;
                else return false;
            return true;
        }
        abstract int getLevel(int[] arg1);
        boolean rightHere(int number, int[] range)
        {
            if(number >= range[0] && number <= range[1])
                return true;
            return false;
        }
    }
    public class DoubleLottery extends Lottery{
        @SuppressWarnings("empty-statement")
        DoubleLottery()
        {
            beforeCount = 6; afterCount = 1;
            beforenumber = new int[beforeCount];
            afternumber = new int[afterCount];
            beforeRange[0] = 1; beforeRange[1] = 33;
            afterRange[0] = 1; afterRange[1] = 16;
            winbnumber=new int[]{3,7,9,22,27,33};
            winanumber=new int[]{12};
        }
        @Override
        int getLevel(int[] arg1) {
            Arrays.sort(arg1, 0, beforeCount);
            Arrays.sort(arg1, beforeCount + 1, beforeCount + afterCount);
            int i = 0, j = 0;
            for(int m = 0; m < beforeCount; m++)
                for(int n = 0; n < beforeCount; n++)
                    if(arg1[m] == winbnumber[n]) 
                        {
                            i++;
                            break;
                        }
            for(int m = 0; m < afterCount; m++)
                for(int n = 0; n < afterCount; n++)
                    if(arg1[m + beforeCount] == winanumber[n]) 
                        {
                            j++;
                            break;
                        }	
            switch(i)
            {
                case 6: if(j == 1) return 1; return 2;
                case 5: if(j == 1) return 3; return 4;
                case 4: if(j == 1) return 4; return 5;
                case 3: if(j == 1) return 5; return 7;
                case 2: if(j == 1) return 6; return 7;
                case 1: if(j == 1) return 6; return 7;
                case 0: if(j == 1) return 6; return 7;
            }
            return 7;
        }
    }
    class BigLottery extends Lottery{
        BigLottery()
        {
            beforeCount = 5; afterCount = 2;
            beforenumber = new int[beforeCount];
            afternumber = new int[afterCount];
            beforeRange[0] = 1; beforeRange[1] = 35;
            afterRange[0] = 1; afterRange[1] = 12;
            winbnumber=new int[]{3,7,9,17,27};
            winanumber=new int[]{6,12};
        }
        @Override
        int getLevel(int[] arg1) {
            Arrays.sort(arg1, 0, beforeCount);
            Arrays.sort(arg1, beforeCount + 1, beforeCount + afterCount);
            int i = 0, j = 0;
            for(int m = 0; m < beforeCount; m++)
                for(int n = 0; n < beforeCount; n++)
                    if(arg1[m] == winbnumber[n]) 
                        {
                            i++;
                            break;
                        }
                for(int m = 0; m < afterCount; m++)
                    for(int n = 0; n < afterCount; n++)
                        if(arg1[m + beforeCount] == winanumber[n]) 
                            {
                                j++;
                                break;
                            }	
            switch(i)
            {
                case 5: if(j == 2) return 1; if(j == 1) return 2; return 3;
                case 4: if(j == 2) return 3;  if(j == 1) return 4; return 5;
                case 3: if(j == 2) return 4; if(j == 1) return 5; return 6;
                case 2: if(j == 2) return 5; if(j == 1) return 6; return 7;
                case 1: if(j == 2) return 6; return 7;
                case 0: if(j == 2) return 6; return 7;
            }
            return 7;
        }
    }
}
