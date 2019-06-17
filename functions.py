from pprint import pprint as pp
def post_list(postIdDict):
    pp(postIdDict)
    postHyperLink = []
    post_group = {}

    for item in sorted(postIdDict, key=lambda x: postIdDict[x][1]['post_group']):
        if postIdDict[item][1]['post_group'] not in post_group:
            post_group[postIdDict[item][1]['post_group']] = ['## '+postIdDict[item][1]['post_group'],[]]

    for item in sorted(postIdDict, key=lambda x: postIdDict[x][1]['post_title']):
        item_group = postIdDict[item][1]['post_group']
        post_group[item_group][1].append('* ['+postIdDict[item][1]['post_title']+']'+'('+postIdDict[item][0]+')')

    for item in sorted(post_group.keys()):
        postHyperLink.append(post_group[item][0]+'\n'+'\n'.join(sorted(post_group[item][1])))
        
    postHyperLink = '\n'.join(postHyperLink)
    return postHyperLink
