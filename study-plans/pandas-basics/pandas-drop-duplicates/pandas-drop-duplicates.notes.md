Just remember that fact the drop_duplicates() is just an alternate for doing negation on duplicated(). For instance, 



df.drop_duplicates() is same as df[~df.duplicated()]



Under the hood it is just an boolean mask. But, it uses hash map to check whether it key is already there are not. So, for every look-up we spend O(1) and we do that n elements (n rows) so therefore it costs us O(n)